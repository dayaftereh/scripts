#include "include/params.h"

static struct option params_options[] =
{
  {"help", no_argument, NULL, 'h'},
  {"verbose", no_argument, NULL, 'v'},
  {"config", required_argument, NULL, 'c'},
  {"pidfile", required_argument, NULL, 'p'}
};

// ----------------------------------------------------------------------------

void params_init(struct Params *params){
  params->verbose = 0;
  params->pid_file = NULL;
  params->config_file = NULL;
}

// ----------------------------------------------------------------------------

ParamsError params_read(struct Params *params, int argc, char* argv[]){
  char opt;
  int index;
  while((opt = getopt_long (argc, argv, "hvc:p:", params_options, &index)) != -1){
    switch (opt) {
      case 'v':
        params->verbose = 1;
        break;
      case 'c':
        params->config_file = strdup(optarg);
        break;
      case 'p':
        params->pid_file = strdup(optarg);
        break;
      case 'h':
        return PARAMS_HELP;
      default:
        return PARAMS_OK;
    }
  }
  return PARAMS_OK;
}

// ----------------------------------------------------------------------------

void params_help(){
  printf("%s v.%s\n", proc_name, version);
  printf("usage:");
  for(int i = 0; i <4;i++){
    struct option o = params_options[i];
    if(o.has_arg == no_argument){
      printf(" [ --%s ]", o.name);
    } else {
      printf(" --%s PATH", o.name);
    }
  }
  printf("\n\n");

  printf("--%s PATH\t\tthe path to the pidfile\n", params_options[3].name);
  printf("--%s PATH\t\tthe path to configuration file\n", params_options[2].name);
  printf("--%s\t\tprints debug output\n", params_options[1].name);
  printf("--%s\t\t\tshow this help message and exit\n", params_options[0].name);
}

// ----------------------------------------------------------------------------

ParamsError params_check(struct Params *params){
  if(params->config_file == NULL){
    fprintf(stderr, "--> missing argument --config\n");
    return PARAMS_ERROR;
  }

  if(params->pid_file == NULL){
    fprintf(stderr, "--> missing argument --pidfile\n");
    return PARAMS_ERROR;
  }

  return PARAMS_OK;
}
