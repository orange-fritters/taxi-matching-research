import java.util.ArrayList;

public class Node {

    public String ID;
    public String name;
    public ArrayList<Edge> cntEdges;
    public double cost;
    public String prev;

    public Node(String ID, String name) {
        this.ID = ID;
        this.name = name;
        this.cntEdges = new ArrayList<Edge>();
        this.cost = Integer.MAX_VALUE;
        this.prev = null;
    }

    public void addEdge(Edge newEdge) {
        cntEdges.add(newEdge);
    }

    public void init() {
        this.cost = Integer.MAX_VALUE;
        this.prev = null;
    }
}
