import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;

import java.io.File;
import java.io.PrintWriter;

public class Main {
    public static void main(String[] args) throws Exception {
        File crawlStorage = new File("src/test/resources/crawler4j");
        CrawlConfig config = new CrawlConfig();

        config.setMaxPagesToFetch(130);
        config.setCrawlStorageFolder(crawlStorage.getAbsolutePath());

        PageFetcher pageFetcher = new PageFetcher(config);
        RobotstxtServer robotstxtServer = new RobotstxtServer(new RobotstxtConfig(), pageFetcher);
        CrawlController controller = new CrawlController(config, pageFetcher, robotstxtServer);

        controller.addSeed("https://medium.com/");

        CrawlController.WebCrawlerFactory<HtmlWebCrawler> factory = HtmlWebCrawler::new;

        controller.start(factory, 20);

        PrintWriter writer = new PrintWriter("/Users/amourety/Desktop/INFO/WebParserCrawler/src/result/" + "" + "index.txt" + "", "UTF-8");

        int index = 1;

        for (String s : HtmlWebCrawler.urlList) {
            writer.println("page" + index + ".txt : " + s);
            index++;
        }

        writer.close();
    }
}
