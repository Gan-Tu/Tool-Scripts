# Introduction
This **bash script** helps you to set up your local machines and servers, so you can ssh into machine directly by typing custom quick-access alias and without the need of typing your password.

# Explanation
Usually, when you use "ssh," you type
```
$ ssh userName@hostName
```

In the following tutorial, I will use "test@hello.world.cs.edu" as an example.

- **Server**: example.com or your IP address. __For example: hello.world.cs.edu__
- **Username**: This depends on which user you chose to enable. The root username is just root. Your domain FTP user or a different sudo user will have a custom name depending on what you typed when you created the user. __For example: test.__
- **Password**: This depends on which user you chose to enable. The root and sudo articles above show how to set a password for those users. The domain FTP user will have the same password that you use for FTP.
- A **alias** you want to use to replace the remote address. __For example: myServer__

# Setting Up
Run the following code in your terminal under the directory where you saved the 'ssh_access_password_free_setup.sh' file.
```
$ chmod +x ssh_access_password_free_setup.sh
$ bash ssh_access_password_free_setup.sh
```

Then, just follow the directions. 
- When prompted for password, type your password. You may need to do so **four** times in the process. 
- When prompted for other input, just simply hit return.

# Future Use
Now, after setting up, you can ssh into your remote address/server by simply typing
```
$ ssh myServer
```

