# Introduction
This **bash script** helps you to set up your local machines and servers, so you can ssh into machine directly by typing custom quick-access alias and without the need of typing your password.

# Explaination
Usually, when you use "ssh," the remote address you type is in the form of 
```
userName@hostName
```

In the following tutorial, I will use "test@hello.world.cs.edu" as an example.

# Prepare Beforehand
- Your server host name. For example: hello.world.cs.edu
- Your user name. For example: test.
- Your password to the server, if any.
- A alias you want to use to replace the remote address. For example: myServer

# Setting Up
Run the following code in your terminal under the directory where you saved the 'ssh_access_password_free_setup.sh' file.
```
chmod +x ssh_access_password_free_setup.sh
./ssh_access_password_free_setup.sh
```

Then, just follow the directions. When prompted for password, type your password. You may need to do so **four** times in the process. When prompted for other input, just simply hit return.

# Future Use
Now, after setting up, you can ssh into your remote address/server by simply typing
```
ssh myServer
```

