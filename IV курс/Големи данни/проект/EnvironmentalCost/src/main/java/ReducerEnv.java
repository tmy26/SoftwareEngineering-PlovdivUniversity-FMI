import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

public class ReducerEnv extends MapReduceBase
        implements org.apache.hadoop.mapred.Reducer<Text, DoubleWritable, Text, Text> {

    private String mode;

    @Override
    public void configure(JobConf job) {
       
        mode = job.get("mode", "total").trim().toLowerCase();
    }

    @Override
    public void reduce(Text key, Iterator<DoubleWritable> values, OutputCollector<Text, Text> output, Reporter reporter)
            throws IOException {

        double sum = 0;
        int count = 0;
       
        while (values.hasNext()) {
            sum += values.next().get();
            count++;
        }
       
        String result;
        switch (mode) {
            case "avg":
                result = String.format("Average: %.2f", (count > 0 ? sum / count : 0));
                break;
            case "total":
            default:
                result = String.format("Total: %.2f", sum);
                break;
        }
    
        output.collect(key, new Text(result));
    }
}
