#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>
#include<unistd.h>
#include"steamcurses.h"
/*//Probably I'll make a class to deal with all the path and commands to run the games
class read_path {
    public:
        
        char *read();
        
};*/
void launch_game_cmd(char* cmd) {
  // Fork off the game on a new thread
  pid_t pid;
  if((pid = fork()) < 0) {
    perror("Forking Error!");
    exit(1);
  }
  if(pid == 0) {
    // Pipe stderr -> stdout -> logfile
    //dup2(fileno(g_logfile), fileno(stdout));
    dup2(fileno(stdout), fileno(stderr));
    system(cmd);
    exit(0);
  }
}

void launch_wine_game(char *path,char* appid, char* username, char* password) {
  char cmd[1024];
  snprintf(cmd,1024, "wine %sSteam.exe -silent -login %s %s -applaunch %s",path ,username, password, appid);
  printf("cmd:%s\n",cmd);
  launch_game_cmd(cmd);
  //system(cmd);
  //free(cmd);
}

int main(int argc,char *argv[]){
    char *path,*read_path;
    FILE *steam_wine = fopen("config","r+");
    if(steam_wine == NULL){
        perror("Error");
        return -1;
    }
    
    size_t len = 0;
	int read;
    
    while ((read = getline(&read_path, &len, steam_wine)) != -1) {
		if(read_path == NULL)	return -1;
        path = strsep(&read_path,"=");
        read_path[(strlen(read_path)-1)] = '\0';// Remove the '\n' command
        //printf("Caminho:%s\n",read_path);
        launch_wine_game(read_path,"227600","calebe945","calebe100");
 	}
	fclose(steam_wine)	;
}
