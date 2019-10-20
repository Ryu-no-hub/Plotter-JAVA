package sample;

import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.scene.paint.Color;
import java.awt.*;
import java.io.*;
import java.util.Vector;

public class Main extends Application {

    private Desktop desktop = Desktop.getDesktop();
    Stage window;
    File file;

    boolean r = false, f = false;
    @Override
    public void start(Stage stage) throws Exception {
        window = stage;
        window.setTitle("Plots Maker");


        GridPane grid = new GridPane();
        grid.setPadding(new Insets(10, 10, 10, 10));
        grid.setHgap(10);
        grid.setVgap(7);
        final FileChooser fileChooser = new FileChooser();

        TextField funcInput = new TextField();
        TextField rangeInput = new TextField();

        funcInput.setMaxWidth(400);
        funcInput.setMinWidth(300);
        funcInput.setPromptText("x/cos(x)");

        rangeInput.setMaxWidth(50);
        rangeInput.setPromptText("20");

        Label firstLabel = new Label("Function: y = ");
        firstLabel.setMinWidth(75);
        Label secondLabel = new Label("Range: ");
        Label statusLabel = new Label("Status ");
        statusLabel.setTextFill(Color.GRAY);

        Button plot = new Button("Plot!");
        Button plotFromFile = new Button("Plot from file!");
        Button fileSelect = new Button("Select file");
        Button funcSave = new Button("Save to file");

        TextArea textArea = new TextArea();
        //textArea.setMinHeight(20);
        //textArea.setMaxHeight(20);
        textArea.setMaxWidth(270);

        ListView<String> listView = new ListView<>();
        listView.getSelectionModel().setSelectionMode(SelectionMode.SINGLE);
        //listView.setMinHeight(40);
        //listView.setMaxHeight(40);

        HBox layout = new HBox();
        HBox hbuttons = new HBox();
        hbuttons.getChildren().addAll(plot, funcSave);
        hbuttons.setSpacing(10);
        VBox inputManage = new VBox();
        VBox fileManage = new VBox();

        GridPane.setConstraints(firstLabel, 0, 1);
        GridPane.setConstraints(funcInput, 1, 1);
        GridPane.setConstraints(secondLabel, 0, 0);
        GridPane.setConstraints(rangeInput, 1, 0);
        GridPane.setConstraints(hbuttons, 1, 2);
        GridPane.setConstraints(fileSelect, 0, 3);
        GridPane.setConstraints(textArea, 1, 3);
        GridPane.setConstraints(statusLabel, 0, 2);

        grid.getChildren().addAll(secondLabel, rangeInput, firstLabel, funcInput, statusLabel,
                                    hbuttons, textArea,fileSelect);
        inputManage.getChildren().add(grid);
        fileManage.getChildren().addAll( plotFromFile, listView);
        fileManage.setPadding(new Insets(10, 10, 10, 10));
        fileManage.setSpacing(10);
        layout.getChildren().addAll(inputManage, fileManage);
        layout.setPadding(new Insets(10, 10, 10, 10));

        rangeInput.textProperty().addListener((observable, oldValue, newValue) -> r = rangeChecker(statusLabel, newValue, f));
        funcInput.textProperty().addListener((observable, oldValue, newValue) -> f = funcChecker(statusLabel, newValue, r));

        String[] args = new String[2];
        plot.setOnAction(e -> {
            if(rangeInput.getText().equals("")) {
                AlertBox.display("Error", "Set up range");
                return;
            }
            else if(funcInput.getText().equals("")){
                AlertBox.display("Error", "Write a function");
                return;
            }
            args[0] = funcInput.getText();
            args[1] = rangeInput.getText();

            Drawer.main(args);
            printLog(textArea, "Plot created for " + funcInput.getText()
                    + " with range of " + rangeInput.getText());
        });
        funcSave.setOnAction(e->{
           try(FileWriter writer = new FileWriter(file, true)){
               String str = "\n" + funcInput.getText();
               writer.write(str);
           } catch (IOException er){
               er.printStackTrace();
           } catch (NullPointerException er){
               AlertBox.display("Error", "Select file first");
           }
            listView.getItems().clear();
            for(int i = 0; i < funcList(file.getAbsolutePath()).size();i++)
            {
                listView.getItems().add(funcList(file.getAbsolutePath()).get(i));
            }
            printLog(textArea, "Updated file " + file.getAbsolutePath());
        });

        fileSelect.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent actionEvent) {
                file = fileChooser.showOpenDialog(window);
                if (file != null) {
                    for(int i = 0; i < funcList(file.getAbsolutePath()).size();i++)
                    {
                        listView.getItems().add(funcList(file.getAbsolutePath()).get(i));
                    }
                    printFileLog(textArea, file);

                }
            }
        });

        plotFromFile.setOnAction(e->{
            if(rangeInput.getText().equals("")){
                AlertBox.display("Error", "Set up range");
                return;
            }
            else if(textArea.getText().equals(""))
            {
                AlertBox.display("Error", "Select file");
                return;
            }
            else if(listView.getSelectionModel().getSelectedItem() == null)
            {
                AlertBox.display("Error", "Select function");
                return;
            }
            args[0] = listView.getSelectionModel().getSelectedItem();
            args[1] = rangeInput.getText();
            Drawer.main(args);
            printLog(textArea, "Plot created for " + listView.getSelectionModel().getSelectedItem()
                    + " with range of " + rangeInput.getText());
        });

        window.setScene(new Scene(layout, 650, 300));
        window.show();

    }

    private boolean rangeChecker (Label statusLabel, String newValue, boolean f ){
        try{
            Integer.parseInt(newValue);
            if(f) {
                statusLabel.setText("Plottable!");
                statusLabel.setTextFill(Color.GREEN);
            }
            else
                throw new IOException();
            return true;
        } catch (NumberFormatException e){
            statusLabel.setText("Not plottable");
            statusLabel.setTextFill(Color.RED);
            return false;
        } catch (IOException e){
            return true;
        }

    }
    private boolean funcChecker (Label statusLabel, String newValue, boolean r){
        try{
            if(newValue.equals(""))
                throw new NumberFormatException();
            if(r) {
                statusLabel.setText("Plottable!");
                statusLabel.setTextFill(Color.GREEN);
            }
            else
                throw new IOException();
            return true;
        } catch (NumberFormatException e){
            statusLabel.setText("Not plottable");
            statusLabel.setTextFill(Color.RED);
            return false;
        } catch (IOException e){
            return true;
        }

    }
    private Vector<String> funcList (String path) {
        Vector<String> vec = new Vector<>();
        try(BufferedReader reader = new BufferedReader(new FileReader(path)))
        {
            String x;
            while((x = reader.readLine()) != null)
                vec.add(x);
        } catch(IOException e){
            e.printStackTrace();
        }
        return vec;
    }

    private void printFileLog(TextArea textArea, File file) {
        if (file == null ) {
            return;
        }
            textArea.appendText("Opening file: "+ file.getAbsolutePath() + "\n");
    }
    void printLog(TextArea textArea, String log) {
        if (log == null ) {
            return;
        }
            textArea.appendText(log + "\n");
    }

    public static void main (String[] args){
        launch(args);
    }
}
