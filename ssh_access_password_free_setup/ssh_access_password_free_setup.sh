clear

echo "############### SETTING UP HOST INFO ###############"

# Get Host
echo "Enter the ssh server Host (e.g. cs61a):"
read host
echo -e "You chose: $host\n"


# Get User
echo "what is your username:"
read user
echo -e "You chose: $user\n"

# Get HostName
servers=("ashby.cs.berkeley.edu"  "ssh.ocf.berkeley.edu" "other")
count=1
for server in "${servers[@]}"; do
    echo "$count. $server"
    let count=count+1
done
echo -e "\nwhich server do you want to use: "
read choice

if [ $choice -le ${#servers[@]} ]; then
    if [ $choice -gt 0 ]; then
        host_name=${servers[$choice - 1]}
        if [ $choice -eq ${#servers[@]} ]; then
            echo "enter the host name for your ssh server (cs61a-bcd): "
            read host_name
        fi
    else
        echo "wrong server choice"
        echo "enter the host name for your ssh server: "
        read host_name
    fi
else
    echo "wrong server choice"
    echo "enter the host name for your ssh server: "
    read host_name
fi
echo $host_name
echo -e "You chose: $host_name\n"


clear
echo "############### INITIAL SETUP ###############"
echo "INSTRUCTION: you will need to enter password four times, if prompted"
echo "INSTRUCTION: just press return directly when prompted"
# Start Setting
ssh $user@$host_name eval 'mv ~/.ssh/id_rsa ~/.ssh/old_id_rsa; ssh-keygen -t rsa;'
ssh $user@$host_name eval 'cd ~/.ssh; cat id_rsa.pub >> authorized_keys; chmod 600 authorized_keys; rm id_rsa.pub;'
scp $user@$host_name:.ssh/id_rsa ~/.ssh/"$host"_id_rsa
ssh $user@$host_name eval 'cd ~/.ssh; rm id_rsa;'


# ### Add Info to .ssh
# cd ~/.ssh
# cat "Host "
cd ~/.ssh
echo -e "\n" >> config
echo "Host $host" >> config
echo "HostName $host_name" >> config
echo "User $user" >> config
echo "IdentityFile ~/.ssh/${host}_id_rsa" >> config

clear
echo "############### FINISHED ###############"

