import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

import java.io.IOException;

public class uploadFileToHDFS {


	    public static void main(String[] args) {
	        // HDFS Configuration
	        Configuration conf = new Configuration();
	        conf.set("fs.defaultFS", "hdfs://localhost:9000"); 

	        String localFilePath = "C:\\Users\\vasko\\Downloads/5.csv"; // Path to the local file
	        String hdfsDestPath = "/user/vasko/input/5.csv"; // HDFS destination path

	        try {
	            // Get the HDFS FileSystem instance
	            FileSystem fs = FileSystem.get(conf);

	            // Upload the file to HDFS
	            fs.copyFromLocalFile(new Path(localFilePath), new Path(hdfsDestPath));
	            System.out.println("File uploaded successfully to HDFS: " + hdfsDestPath);

	            // Close the FileSystem
	            fs.close();
	        } catch (IOException e) {
	            System.err.println("Exception while uploading file to HDFS: " + e.getMessage());
	            e.printStackTrace();
	        }
	    }
	}
