import java.io.*;
import java.util.*;

public class Graph {

    private static HashMap<String, Node> graph;
    private static HashMap<String, Double> speedList;

    public static void main(String args[]) throws IOException {
        BufferedReader fr = new BufferedReader(new FileReader("data.txt"));

        String fLine;
        graph = new HashMap<>();
        speedList = new HashMap<>();

        // .txt 파일로부터 [nodeID] [이름] 입력
        while ((fLine = fr.readLine()) != null) {
            String[] stationInfo = fLine.split(" ", 2);
            if (stationInfo.length != 2)
                break;
            String ID = stationInfo[0];
            String name = stationInfo[1];

            Node newNode = new Node(ID, name);
            Node node = graph.get(ID);
            if (node == null)
                graph.put(ID, newNode);
        }

        // .txt 파일로부터 [edgeID] [속력] 입력
        while ((fLine = fr.readLine()) != null) {
            String[] speedInfo = fLine.split(" ", 2);
            if (speedInfo.length != 2)
                break;
            String ID = speedInfo[0];
            String speed_str = speedInfo[1];
            Double speed = Double.valueOf(speed_str);

            speedList.put(ID, speed);
        }

        // .txt 파일로부터 [fNodeID] [tNodeID] [edgeID] [거리] 입력
        while ((fLine = fr.readLine()) != null) {
            String[] edgeInfo = fLine.split(" ", 4);
            if (edgeInfo.length != 4)
                break;
            String fNodeID = edgeInfo[0];
            String tNodeID = edgeInfo[1];
            String edgeID = edgeInfo[2];
            String distance_str = edgeInfo[3];
            Double distance = Double.valueOf(distance_str);

            Double speed = speedList.get(edgeID);
            Node fNode = graph.get(fNodeID);
            if (fNode != null && speed != null) {
                Edge newEdge = new Edge(fNodeID, tNodeID, distance, speed);
                fNode.cntEdges.add(newEdge);
            }
        }

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        while (true) {
            try {
                String input = br.readLine();
                if (input.compareTo("QUIT") == 0)
                    break;

                command(input);
            } catch (IOException e) {
                System.out.println("입력이 잘못되었습니다. 오류 : " + e.toString());
            }
        }
    }

    private static void command(String input) throws IOException {
        String[] inputArray = input.split(" ", 2);
        String fNodeID = inputArray[0];
        String tNodeID = inputArray[1];

        PriorityQueue<Node> queue = new PriorityQueue<>(Comparator.comparingDouble(node -> node.cost));
        HashMap<String, Node> visitedNodes = new HashMap<>();
        HashMap<String, Node> modifiedNodes = new HashMap<>();

        Node fNode = graph.get(fNodeID);
        fNode.cost = 0;
        queue.add(fNode);
        modifiedNodes.put(fNode.ID, fNode);

        Node lastNode = null;
        while (!queue.isEmpty()) {
            Node currentNode = queue.poll();
            visitedNodes.put(currentNode.ID, currentNode);

            if (tNodeID.equals(currentNode.ID)) {
                lastNode = currentNode;
                break;
            }

            for (Edge edge : currentNode.cntEdges) {
                Node nextNode = graph.get(edge.tNodeID);
                if (visitedNodes.containsKey(nextNode.ID))
                    continue;

                double newCost = currentNode.cost + edge.cost;
                if (newCost < nextNode.cost) {
                    nextNode.cost = newCost;
                    nextNode.prev = edge.fNodeID;
                    queue.add(nextNode);
                    modifiedNodes.put(nextNode.ID, nextNode);
                }
            }
        }

        if (lastNode == null) {
            System.out.println("Cannot find a path from " + fNodeID + " to " + tNodeID);
            for (Node node : modifiedNodes.values())
                node.init();
            return;
        }

        // 도착지부터 출발지까지 prev 토대로 경로 작성
        ArrayList<String> path = new ArrayList<>();
        Node currentNode = lastNode;
        Node prevNode;
        while (currentNode.prev != null) {
            prevNode = graph.get(currentNode.prev);
            path.add(0, currentNode.name);
            currentNode = visitedNodes.get(prevNode.ID);
        }
        path.add(0, currentNode.name);

        // 경로 출력
        System.out.println(lastNode.cost);

        // 방문한 node 초기화
        for (Node node : modifiedNodes.values())
            node.init();
    }
}
