import java.io.File;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

import java.math.BigInteger;

import java.io.IOException;
import java.io.File;
import java.nio.file.Path;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;

import java.security.MessageDigest;
import java.security.DigestInputStream;
import java.security.NoSuchAlgorithmException;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Scanner;


public class ListDuplicate {

    /** Root directory. */
    private File root;


    public ListDuplicate(String pathname) {
        root = new File(pathname);
    }

    /** Return all duplicate files grouped together. */
    public List<List<String>> findDuplicates() {
        if (!root.canRead()) {
            throw new IllegalStateException("cannot read root directory");
        } else if (!root.isDirectory()) {
            throw new IllegalStateException("root file is not a directory");
        }

        List<List<File>> groups = groupBySize(root);
        List<List<File>> filtered = filterByHash(groups);
        List<List<File>> duplicates = fullComparision(filtered);

        ArrayList<List<String>> result = new ArrayList<List<String>>();
        for (List<File> group: duplicates) {
            if (group.size() <= 1) {
                continue;
            }
            ArrayList<String> d = new ArrayList<String>();
            for (File f : group) {
                d.add(f.getPath());
            }
            result.add(d);
        }

        return result;
    }

    /** Return all files under ROOT directory grouped together by size.
     *  Each group has at least 2 files.
     *  Assumes root is indeed a directory and readable. */
    private List<List<File>> groupBySize(File root) {
        HashMap<Long, ArrayList<File>> visited = new HashMap<Long, ArrayList<File>>();
        HashSet<File> directoryVisited = new HashSet<File>();
        groupBySize(root, visited, directoryVisited);
        ArrayList<List<File>> groups = new ArrayList<List<File>>();
        for (Long size : visited.keySet()) {
            if (visited.get(size).size() > 1) {
                groups.add(visited.get(size));
            }
        }
        return groups;
    }
    
    /** Save all files under ROOT directory grouped together by size to VISITED.
     *  Visited directory in DIRECTORYVISITED won't be visited again.
     *  Assumes root is indeed a directory and readable. */
    private void groupBySize(File root, HashMap<Long, ArrayList<File>> visited,
            HashSet<File> directoryVisited) {
        try {
            if (directoryVisited.contains(root)) {
                return;
            }
            directoryVisited.add(root);
            for (File f : root.listFiles()) {
                if (!f.canRead()) {
                    /** Do something with it? */
                } else if (f.isDirectory()) {
                    groupBySize(f, visited, directoryVisited);
                } else if (visited.containsKey(f.length())) {
                    visited.get(f.length()).add(f);
                } else {
                    ArrayList<File> group = new ArrayList<File>();
                    group.add(f);
                    visited.put(f.length(), group);
                }
            }
        } catch (SecurityException e) {
            System.out.println(e);
        }
    }


    /** Return files whose content hashcode is not the same within each group of GROUPS. */
    private List<List<File>> filterByHash(List<List<File>> groups) {
        ArrayList<List<File>> result = new ArrayList<List<File>>();
        for (List<File> group: groups) {
            HashMap<Long, ArrayList<File>> files = new HashMap<Long, ArrayList<File>>();
            for (File f : group) {
                long hash = hashContentRough(f);
                if (!files.containsKey(hash)) {
                    files.put(hash, new ArrayList<File>());
                }
                files.get(hash).add(f);
            }
            for (Long hash : files.keySet()) {
                if (files.get(hash).size() > 1) {
                    result.add(files.get(hash));
                }
            }
        }
        return result;
    }

    /** Return duplicate files combined together within each group of GROUPS.
     *  Each group may contain only 1 file. */
    private List<List<File>> fullComparision(List<List<File>> groups) {
        ArrayList<List<File>> result = new ArrayList<List<File>>();
        for (List<File> group: groups) {
            HashMap<Long, ArrayList<File>> files = new HashMap<Long, ArrayList<File>>();
            for (File f : group) {
                long hash = hashContentComplete(f);
                if (!files.containsKey(hash)) {
                    files.put(hash, new ArrayList<File>());
                }
                files.get(hash).add(f);
            }
            for (Long hash : files.keySet()) {
                if (files.get(hash).size() > 1) {
                    result.add(files.get(hash));
                }
            }
        }
        return result;
    }

    /** Return a rough hashcode of the FILE content. */
    private long hashContentRough(File file) {
        Path path = file.toPath();
        final int numBytesToReadPerSample = 4000;
        final long totalBytes = new File(path.toString()).length();

        InputStream inputStream = null;
        MessageDigest digest = null;

        try {
            inputStream = new FileInputStream(path.toString());
            digest = MessageDigest.getInstance("SHA-512");
        } catch (FileNotFoundException e) {
            System.out.println(e);
        } catch (NoSuchAlgorithmException e) {
            System.out.println(e);
        }

        DigestInputStream digestInputStream = new DigestInputStream(inputStream, digest);

        try {

            // if the file is too short to take 3 samples, hash the entire file
            if (totalBytes < numBytesToReadPerSample * 3) {
                byte[] bytes = new byte[(int) totalBytes];
                digestInputStream.read(bytes);
            } else {
                byte[] bytes = new byte[numBytesToReadPerSample * 3];
                long numBytesBetweenSamples = (totalBytes - numBytesToReadPerSample * 3) / 2;

                // read first, middle and last bytes
                for (int n = 0; n < 3; n++) {
                    digestInputStream.read(bytes, n * numBytesToReadPerSample, numBytesToReadPerSample);
                    digestInputStream.skip(numBytesBetweenSamples);
                }
            }
        } catch (IOException e) {
            System.out.println(e);
        }
        return new BigInteger(1, digest.digest()).toString(16).toString().hashCode();
    }

    /** Return a hashcode of the FILE content. */
    private long hashContentComplete(File file) {
        Path path = file.toPath();
        final int numBytesToReadPerSample = 4000;
        final long totalBytes = new File(path.toString()).length();

        InputStream inputStream = null;
        MessageDigest digest = null;

        try {
            inputStream = new FileInputStream(path.toString());
            digest = MessageDigest.getInstance("SHA-512");
        } catch (FileNotFoundException e) {
            System.out.println(e);
        } catch (NoSuchAlgorithmException e) {
            System.out.println(e);
        }

        DigestInputStream digestInputStream = new DigestInputStream(inputStream, digest);

        try {

            byte[] bytes = new byte[(int) totalBytes];
            digestInputStream.read(bytes);
        } catch (IOException e) {
            System.out.println(e);
        }
        return new BigInteger(1, digest.digest()).toString(16).toString().hashCode();
    }

    /** Return true iff two files F1 and F2 are completedly the same. */
    private boolean compare(File f1, File f2) {
        try {
            BufferedReader reader1 = new BufferedReader(new FileReader(f1));
            BufferedReader reader2 = new BufferedReader(new FileReader(f1));
            int char1 = 0, char2 = 0;
            boolean finished = false;
            while (!finished) {
                char1 = reader1.read();
                char2 = reader2.read();
                if (char1 != char2) {
                    return false;
                } else if (char1 == -1) {
                    finished = true;
                }
            }
        } catch (FileNotFoundException e) {
            System.out.println(e);
        } catch (IOException e) {
            System.out.println(e);
        }
        return true;
    }

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        System.out.println("path:");
        ListDuplicate s = new ListDuplicate(in.nextLine());
        List<List<String>> result = s.findDuplicates();
        int index = 0;
        System.out.println();
        for (List<String> group: result) {
            System.out.println("group " + index + ":");
            for (String name: group) {
                System.out.println(name);
            }
            System.out.println();
            index++;
        }
    }
}