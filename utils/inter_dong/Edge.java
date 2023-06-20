public class Edge {

    public String fNodeID;
    public String tNodeID;
    public double cost;

    public Edge(String fNodeID, String tNodeID, double distance, double speed) {
        this.fNodeID = fNodeID;
        this.tNodeID = tNodeID;
        this.cost = distance / speed;
    }
}
