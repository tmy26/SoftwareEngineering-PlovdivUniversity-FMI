import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.URI;
import javax.swing.*;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.*;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;

public class App extends JFrame {

	// GUI Components
	private final JTextField yearField = new JTextField(10);
	private final JTextField sectorField = new JTextField(10);
	private final JTextField unitsField = new JTextField(10);
	private final JTextArea resultOutput = new JTextArea(35, 40);

	public static void main(String[] args) {
		SwingUtilities.invokeLater(App::new);
	}

	public App() {
		setupGUI();
	}

	private void setupGUI() {
		// Set up JFrame properties
		setTitle("Environmental Data Analysis");
		setSize(840, 700);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		// Main panel layout
		JPanel panel = new JPanel(new FlowLayout());

		// Add input fields and buttons
		panel.add(new JLabel("Year:"));
		panel.add(yearField);
		panel.add(new JLabel("Sector:"));
		panel.add(sectorField);
		panel.add(new JLabel("Units:"));
		panel.add(unitsField);

		JButton searchButton = new JButton("Search");
		JButton avgButton = new JButton("Calculate Avg");
		panel.add(searchButton);
		panel.add(avgButton);

		// Add output area
		resultOutput.setEditable(false);
		JScrollPane scrollPane = new JScrollPane(resultOutput);
		scrollPane.setPreferredSize(new Dimension(600, 500));
		panel.add(scrollPane);

		add(panel);
		setVisible(true);

		// Action listeners for buttons
		searchButton.addActionListener(e -> executeHadoopJob("total"));
		avgButton.addActionListener(e -> executeHadoopJob("avg"));
	}

	private void executeHadoopJob(String mode) {

		String year = yearField.getText().trim();
		String sector = sectorField.getText().trim();
		String units = unitsField.getText().trim();

		runHadoopJob(year, sector, units, mode);
	}

	private void runHadoopJob(String year, String sector, String units, String mode) {
		Configuration conf = new Configuration();
		conf.set("mode", mode);

		Path inputPath = new Path("hdfs://127.0.0.1:9000/user/vasko/input/5.csv");
		Path outputPath = new Path("hdfs://127.0.0.1:9000/result");

		JobConf job = new JobConf(conf, App.class);
		job.set("year", year);
		job.set("sector", sector);
		job.set("units", units);
		job.setMapperClass(MapperEnv.class);
		job.setReducerClass(ReducerEnv.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(DoubleWritable.class);

		try {
			FileSystem fs = FileSystem.get(URI.create("hdfs://127.0.0.1:9000"), job);

			// Delete previous output if exists
			if (fs.exists(outputPath)) {
				fs.delete(outputPath, true);
			}

			FileInputFormat.setInputPaths(job, inputPath);
			FileOutputFormat.setOutputPath(job, outputPath);

			// Run the job
			RunningJob runningJob = JobClient.runJob(job);
			if (runningJob.isSuccessful()) {
				displayResults(fs, outputPath);
			} else {
				showError("Hadoop job failed.");
			}

		} catch (IOException e) {
			showError("Error running Hadoop job: " + e.getMessage());
		}
	}

	private void displayResults(FileSystem fs, Path outputPath) {
		try {
			// Clear any previous results
			resultOutput.setText("");

			// Iterate over the files in the output path
			for (FileStatus file : fs.listStatus(outputPath)) {

				// Check if the file is a part of the output
				if (file.getPath().getName().startsWith("part-")) {
					try (BufferedReader br = new BufferedReader(new InputStreamReader(fs.open(file.getPath())))) {

						String line;
						// Read each line from the file and append it to resultOutput

						while ((line = br.readLine()) != null) {
							resultOutput.append(line + "\n");
						}
					} catch (IOException e) {
						showError("Error reading the file: " + e.getMessage());
					}
				}
			}
		} catch (IOException e) {
			showError("Error listing Hadoop results: " + e.getMessage());
		}
	}

	private void showError(String message) {
		JOptionPane.showMessageDialog(this, message, "Error", JOptionPane.ERROR_MESSAGE);
	}
}
