#include "vehicle_animation_sim_capi_host.h"
static vehicle_animation_sim_host_DataMapInfo_T root;
static int initialized = 0;
__declspec( dllexport ) rtwCAPI_ModelMappingInfo *getRootMappingInfo()
{
    if (initialized == 0) {
        initialized = 1;
        vehicle_animation_sim_host_InitializeDataMapInfo(&(root), "vehicle_animation_sim");
    }
    return &root.mmi;
}

rtwCAPI_ModelMappingInfo *mexFunction() {return(getRootMappingInfo());}
