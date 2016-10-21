#!/usr/bin/env groovy
// Spec: in.txt is input string, result written to out.txt, debug to debug.txt,
// injar.jar is the JAR file with LinkGame.getSolutions()
// out.txt is formatted one solution per line

String baseDir = "/srv/mallory";
String input = new File(baseDir + "/in.txt").text.trim();

def debugFile = new File(baseDir + "/debug.txt");
debugFile.write("No data.");

def localFile = new File(baseDir + "/injar.jar");
this.class.classLoader.rootLoader.addURL(localFile.toURI().toURL());

try {
    String[] output = Class.forName("comp1110.ass2.LinkGame").getSolutions(input);
    PrintWriter outFile = new PrintWriter(baseDir + "/out.txt");
    if (output != null) {
        for (String sol : output) {
            outFile.write(sol);
            outFile.write("\n");
        }
        outFile.close()
    } else {
        debugFile.write("LinkGame.getSolutions() returned null");
        outFile.close()
    }
} catch (Exception e) {
    PrintWriter writer = new PrintWriter(debugFile);
    e.printStackTrace(writer);
    writer.close()

    writer = new PrintWriter(new File(baseDir + "/out.txt"));
    writer.write("!!ERROR!!");
    writer.close();
}
