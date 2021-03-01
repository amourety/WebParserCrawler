import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Set;
import java.util.regex.Pattern;

public class HtmlWebCrawler extends WebCrawler {

    private final static Pattern EXCLUSIONS
            = Pattern.compile(".*(\\.(css|js|xml|gif|jpg|png|mp3|mp4|zip|gz|pdf))$");

    static ArrayList<String> urlList = new ArrayList<>();

    static int index = 0;

    @Override
    public boolean shouldVisit(Page referringPage, WebURL webUrl) {
        String url = webUrl.getURL().toLowerCase();

        return !EXCLUSIONS.matcher(url).matches()
                && url.startsWith("https://medium.com/");
    }

    @Override
    public void visit(Page page) {
        String url = page.getWebURL().getURL();

        if (page.getParseData() instanceof HtmlParseData) {
            HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
            String html = htmlParseData.getHtml();
            index++;
            try {
                PrintWriter writer = new PrintWriter("/Users/amourety/Desktop/INFO/WebParserCrawler/src/result/page" + index + ".txt", "UTF-8");
                writer.println(html);
                writer.close();
                urlList.add(url);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
