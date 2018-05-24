#include "__cf_vehicle_animation_sim.h"
#ifndef RTW_HEADER_vehicle_animation_sim_cap_host_h_
#define RTW_HEADER_vehicle_animation_sim_cap_host_h_
#ifdef HOST_CAPI_BUILD
#include "rtw_capi.h"
#include "rtw_modelmap.h"
typedef struct { rtwCAPI_ModelMappingInfo mmi ; }
vehicle_animation_sim_host_DataMapInfo_T ;
#ifdef __cplusplus
extern "C" {
#endif
void vehicle_animation_sim_host_InitializeDataMapInfo (
vehicle_animation_sim_host_DataMapInfo_T * dataMap , const char * path ) ;
#ifdef __cplusplus
}
#endif
#endif
#endif
