import java.io.IOException;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

public class MapperEnv extends MapReduceBase implements Mapper<LongWritable, Text, Text, DoubleWritable> {

    private String yearFilter;
    private String sectorFilter;
    private String unitsFilter;

    @Override
    public void configure(JobConf job) {
        
        yearFilter = job.get("year", "").trim();
        sectorFilter = job.get("sector", "").trim();
        unitsFilter = job.get("units", "").trim();
    }

    @Override
    public void map(LongWritable key, Text value, OutputCollector<Text, DoubleWritable> output, Reporter reporter)
            throws IOException {

        String[] fields = value.toString().split(",");

        String year = fields[0].trim();
        String sector = fields[1].trim();
        String units = fields[5].trim();

        double dataValue;
        try {
            dataValue = Double.parseDouble(fields[8].trim());
        } catch (NumberFormatException e) {
            return;
        }
        
        if ((yearFilter.isEmpty() || year.contains(yearFilter)) &&
            (sectorFilter.isEmpty() || sector.contains(sectorFilter)) &&
            (unitsFilter.isEmpty() || units.contains(unitsFilter))) {
            
            String outputKey = year + "-" + sector + "-" + units;
            output.collect(new Text(outputKey), new DoubleWritable(dataValue));
        }
    }
}
