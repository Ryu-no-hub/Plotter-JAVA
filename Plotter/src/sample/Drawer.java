package sample;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.util.*;
import java.io.*;
import javax.swing.JFrame;
import javax.swing.JPanel;
import static java.lang.Math.*;

public class Drawer extends JPanel  {

    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        this.setBackground(Color.BLACK);

        Graphics2D g2d = (Graphics2D) g;

        g2d.setColor(Color.green);

        g2d.drawLine(0, H/2, W, H/2);
        g2d.drawLine(W/2, 0, W/2, H);

        for(int i = 0;i < 2*range ;i++)
        {
            g2d.drawLine(i * W / (2 * range), H / 2 - 100/range, i * W / (2 * range), H / 2 + 100/range);
            g2d.drawLine(W/2 - 100/range, i * H / (2 * range), W/2 + 100/range, i * H / (2 * range));
        }

        for(int i = 0; i < X.length;i++)
            g2d.drawLine((int)(X[i]*W/(2*range)+W/2), (int)(Y[i]*W/(2*range)+H/2), (int)(X[i]*W/(2*range) + W/2),(int) (Y[i]*W/(2*range) + H/2));

    }

    static double[] X; // х координаты
    static double[] Y; // у координаты
    static int W = 740;
    static int H = 740;
    static double step = 0.01;
    private static int range;


    static void mydisplay(int size, String[] args) {

        Drawer points = new Drawer();
        JFrame frame = new JFrame("Plot");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(points);
        frame.setSize(W, H);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);

    }

    public static boolean check_iter_num(char c) {
        if (c == '0' || c == '1' || c == '2' || c == '3' || c == '4' ||	c == '5' ||
                c == '6' || c == '7' || c == '8' || c == '9' || c == '.')
            return true;
        return false;
    }

    public static double LetterFunctions(String func, double num) {
        System.out.println(func + " " + num);
        switch(func){
            case("sin"):
                return sin(num);
            case("cos"):
                return cos(num);
            case("tan"):
                return tan(num);
            case("ctg"):
                return 1 / tan(num);
            case("asin"):
                return asin(num);
            case("acos"):
                return acos(num);
            case("atan"):
                return atan(num);
            case("abs"):
                return abs(num);
            case("exp"):
                return exp(num);
        }

        return 0;
    }

    public static String x_substitute(double x, String equation_s) {
        StringBuffer equation = new StringBuffer(equation_s);
        for (int i = 0; i < equation.length(); i++)
        {
            char c = equation.charAt(i);
            if (c == 'x' && i+1 <equation.length() && equation.charAt(i+1) != 'p'){
                equation = equation.delete(i, i+1);
                String ar;
                if (x < 0)
                    ar = "(" + x + ")";
                else
                    ar = Double.toString(x);
                equation.insert(i, ar);
                //i += toString(x).length() - 2;
                //cout << x << ", " << to_string(x).size() << endl;
            }
        }
        return new String(equation);
    }

    static double operate(double left, char op, double right) {
        if (op == '+')
            return left + right;
        else if (op == '-')
            return left - right;
        else if (op == '*')
            return left * right;
        else if (op == '/')
            return left / right;
        else if (op == '^')
            return pow(left, right);
        else return 0;
    }

    static boolean check_continue_string(char c, int br) {
        if (c != '-' && c != '+'){
            return true;
        }
        else if (br == 0)
            return false;
        else return true;
    }

    static String next_operand_string(String equation) {
        StringBuffer res = new StringBuffer();
        int br = 0;
        for (int i = 0; i < equation.length() && check_continue_string(equation.charAt(i), br); i++)
        {
            char c = equation.charAt(i);
            if (c == '(')
                br++;
            else if (c == ')')
                br--;
            res.append(c);
        }
        //cout << "next operand string = " << result << endl;
        return new String(res);
    }

    static double calculate(String equation) {
        double num = 0;
        for (int i = 0; i < equation.length();i++)
        {
            char c = equation.charAt(i);
            if (check_iter_num(c)) {
                String number = "";
                if (c == '-')
                    number += c;
                for (i=i; i < equation.length() && check_iter_num(equation.charAt(i)); i++)
                    number += equation.charAt(i);
                i--;
                num = Double.parseDouble(number);
            }
            else if (c == '+' || c == '-' || c == '*' || c == '/' || c == '^')
            {
                String next_str = next_operand_string(equation.substring(++i));
                num = operate(num, equation.charAt(--i), calculate(next_str));
                i += next_str.length();
            }
            else if (c == 's' || c == 'c' || c == 't' || c == 'a' || c == 'e'){
                String trigon_func = "", argument = "";
                while (equation.charAt(i) != '(')
                    trigon_func += equation.charAt(i++);
                i++;
                int br = 1;
                for (i=i; br != 0; i++) {
                    if (equation.charAt(i) == '('){
                        br++;
                        argument += equation.charAt(i);
                    }
                    else if (equation.charAt(i) == ')'){
                        br--;
                        argument += equation.charAt(i);
                        if (br == 0)
                            argument = argument.substring(0, argument.length() - 1);
                    }
                    else argument += equation.charAt(i);
                }
                num = LetterFunctions(trigon_func, calculate(argument));
                i--;
            }
            else if (c == '('){
                i++;
                int br_count = 1;
                String new_equation = "";
                for (i=i; br_count != 0; i++)
                {
                    if (equation.charAt(i) == '('){
                        br_count++;
                        new_equation += equation.charAt(i);
                    }
                    else if (equation.charAt(i) == ')'){
                        br_count--;
                        new_equation += equation.charAt(i);
                        if (br_count == 0)
                            new_equation = new_equation.substring(0, new_equation.length() - 1);
                    }
                    else if (i == equation.length()-1) //cout << "Скобки не закрылись до конца выражения!" << endl;
                    {
                        //Main.printlog();
                        System.out.println("Скобки не закрылись до конца выражения");
                        break;
                    }
                    else new_equation += equation.charAt(i);
                }
                //cout << "Длинна выражения в скобках = " << new_equation.size() << endl;
                num = calculate(new_equation);
                i--;
            }
        }
        return num;
    }


    static double count_Y(double x, String equation) {
        //cout << endl << equation << endl;
        equation = x_substitute(x, equation);
        //cout << endl << equation << endl;
        return calculate(equation);
    }

    static int buildarray(String s) { //1. Буквы тригонометрических функции, 2. Буква х, 3. Скобки, 4. Арифметические действия, 5. Цифры
        Scanner myObj = new Scanner(System.in);
        double beg, end;
//        int step;
//        String start = s.substring(0, 4);
//        if (!start.equals("y = ")) {
//            System.out.println("Выражение имеет неправильный вид:\n" + start + "\n");
//            return 0;
//        }
//        start = s.substring(4);
        System.out.println("Функция: " + s);
        //cin >> beg >> end;
        beg = -range;
        end = range;
//        System.out.println("Шаг по х: (1. - 0.1, 2. - 0.05, 3. - 0.02, 4. - 0.01): ");
//        step = Integer.parseInt(myObj.nextLine());
//        step = Step(step);
        int size = (int) ((end - beg) / step);
//        countd = size;
        X = new double[size+1];
        Y = new double[size+1];
        System.out.println("Точек: " + (size + 1));
        for (int i = 0; i <= size; i++) {
            X[i] = beg + i * step;
        }
        for (int i = 0; i <= size; i++) {
            Y[i] = -count_Y(X[i], s);
        }
        System.out.println("Массивы координат сгенерированы :");
//        for (int i = 0; i <= size; i++)
//            System.out.println("(" + X[i] + ", " + Y[i] + ")\n" );
        return size;
    }

    static Vector<String> funclist(String path) {
        Vector<String> vec = new Vector<>();
        try(BufferedReader reader = new BufferedReader(new FileReader(path))){
            int k = 0;
            String x;
            while ((x = reader.readLine()) != null) {
                System.out.println(++k + ". " + x);
                vec.add(x);
            }
        } catch (IOException e)
        {
            e.printStackTrace();
        }
        return vec;
    }

    public static void main(String[] args) {
        Vector<String> func;
        //String path = "C://file2.txt", x;
        int pointsAmount = 0;

        range = Integer.parseInt(args[1]);
        //System.out.println(range);
        pointsAmount = buildarray(args[0]);
        //System.out.println(pointsAmount);
        mydisplay(pointsAmount, args);

//        System.out.println("1 - Построить функцию из списка\n2 - Построить последнюю функцию\n3 - Ввести и построить новую функцию: ");
//        Scanner com = new Scanner(System.in);
//        command = Integer.parseInt(com.nextLine());
//        System.out.println("command = " + command + "\nДиапазон функции (в каждую сторону): ");
//        range = Integer.parseInt(com.nextLine());
//        switch (command) {
//            case 1:
//                func = funclist(path);
//                System.out.println("Введите номер функции: ");
//                do {
//                    fnum = Integer.parseInt(com.nextLine());
//                    if (fnum > func.size() || fnum < 0) System.out.println("Номера не существует, введите заного: ");
//                    if (fnum == 0) break;
//                } while (fnum > func.size());
//                System.out.println("Построение функции " + func.get(fnum - 1) + "\n\n");
//                pointsAmount = buildarray(func.get(fnum - 1));
//                if (pointsAmount == 0)
//                    System.out.println("Функция не может быть построена\n");
//                else
//                {
//                    mydisplay(pointsAmount, args);
//                }
//                func.clear();
//                break;
//            case 2:
//                try(BufferedReader reader = new BufferedReader(new FileReader(path))){
//                    String str = "";
//                    while ((x = reader.readLine()) != null)
//                        str = x;  // Запись из файла в вектор
//                    pointsAmount = buildarray(str);
//                } catch (IOException e)
//                {
//                    e.printStackTrace();
//                }
//                if (pointsAmount == 0)
//                    System.out.println("Функция не может быть построена\n");
//                else
//                {
//                    mydisplay(pointsAmount, args);
//                }
//                break;
//            case 3:
//                System.out.println("Функция: ");
//                x = com.nextLine();
//                try(FileWriter writer = new FileWriter(path, true)){
//                    writer.write("\n" + x);
//                } catch(IOException e){
//                    e.printStackTrace();
//                }
//                pointsAmount = buildarray(x);
//                if (pointsAmount == 0)
//                    System.out.println("Функция не может быть построена\n");
//                else
//                {
//                    mydisplay(pointsAmount, args);
//                }
//                break;


//                case 4:
//                    funclist(fin, func);
//                    fin.close();
//                    cout << "Номер удаляемой функции: ";
//                    do {
//                        cin >> fnum;
//                        if (fnum > func.size()) cout << "Номера не существует, введите заного: ";
//                    } while (fnum > func.size());
//                    func.erase(func.begin() + fnum - 1);
//                    fout.close();
//                    fout.open(path);
//                    copy(func.begin(), func.end(), ostream_iterator < string > (fout, "\n"));
//                    func.clear();
//                    fout.close();
//                    break;
    }
}