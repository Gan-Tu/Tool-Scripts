import java.util.Stack;
import java.util.HashMap;
import java.io.File;
import java.util.Scanner;

import java.math.BigInteger;

import java.io.File;
import java.nio.file.Path;
import java.io.IOException;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;

import java.security.MessageDigest;
import java.security.DigestInputStream;
import java.security.NoSuchAlgorithmException;


/** A helper tool that clean duplicate files within a specified path.
 *  By default, the tool deletes the duplicate files with the newest modification
 *  time, and it won't delete empty directories after deleting duplicate files.
 *  @author Gan Tu
 */
public class CleanDuplicates{

    public static void main(String[] args) {
        boolean correctPath = false;
        String path = null;
        Scanner in = new Scanner(System.in);
        CleanDuplicates file = null;
        while (!correctPath) {
            System.out.println("enter a path to clean: ");
            path = in.nextLine().trim();
            try {
                file = new CleanDuplicates(path);
                file.delete();
                correctPath = true;
            } catch (NullPointerException e) {
                System.out.println("Incorrect path name");
            }
        }
    }

    /** Path of directory to clean duplicates. */
    private String path;
    /** A stack of all files in the directory. */
    private HashMap<Long, File> files;
    /** A stack of all files to delete. */
    private Stack<File> toDelete;
    
    /** A constructor for Duplicate. Default path is null. */
    public CleanDuplicates() {
        this(null);
    }

    /** A constructor for Duplicate under PATH. */
    public CleanDuplicates(String path) {
        this.path = path;
        this.files = new HashMap<Long, File>();
        this.toDelete = new Stack<File>();
    }

    /** Delete all files. */
    public void delete() {
        if (this.path == null) {
            throw new IllegalStateException("no path is given.");
        }
        scanFiles(this.path, this.files);

        System.out.println("Deleted files:");
        for (File file : toDelete) {
            System.out.println(file.toString());
        }
        System.out.println("done.");

        while (!this.toDelete.isEmpty()) {
            deleteFile(this.toDelete.pop());
        }
    }

    /** Add path of where to delete. Only valid when no path is supplied yet. */
    public void addPath(String path) {
        if (this.path != null) {
            throw new IllegalArgumentException("cannot change path");
        }
        this.path = path;
    }

    /** Hash content of file F. 
     *  @Credit: Interview Cake: 
     *  https://www.interviewcake.com/question/java/find-duplicate-files
     */
    private long hash(File f) {
        Path path = f.toPath();
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

    /** Add the file F ready to be deleted. */
    private void addDelete(File f) {
        this.toDelete.add(f);
    }

    /** Delete the file F. */
    private void deleteFile(File f) {
        f.delete();
    }

    /** Return true if a file is a directory */
    private boolean isDirectory(File f) {
        return f.isDirectory();
    }

    /** Add all files under a PATH to LIST. If duplicate file exists,
     *  add the file that was modified most recently to delete stack. 
     *  Danger: stackoverflow error if too many subdirectories. */
    private void scanFiles(String path, HashMap<Long, File> list) {
        File[] files = allFiles(path);
        long hash;
        for (File f: files) {
            if (isDirectory(f)) {
                scanFiles(toPath(f), list);
            } else {
                hash = hash(f);
                if (list.containsKey(hash)) {
                    if (younger(f, list.get(hash))) {
                        addDelete(f);
                    } else {
                        addDelete(list.get(hash));
                        list.put(hash, f);
                    }
                } else {
                    list.put(hash, f);
                }
            }
        }
    }

    /** Return the path for a directory file F. */
    private String toPath(File f) {
        return f.toString();
    }

    /** Return true if file F1 is younger than file F2. */
    private boolean younger(File f1, File f2) {
        return f1.lastModified() > f2.lastModified();
    }

    /** Return a list of all files, file or directory, under
    the directory specified by PATH. */
    private File[] allFiles(String path) {
        File file = new File(path);
        return file.listFiles();
    }
}