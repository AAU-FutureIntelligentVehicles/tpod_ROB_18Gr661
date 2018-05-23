#include "__cf_vehicle_animation_sim.h"
#ifndef RTW_HEADER_vehicle_animation_sim_h_
#define RTW_HEADER_vehicle_animation_sim_h_
#include <stddef.h>
#include <string.h>
#include "rtw_modelmap.h"
#ifndef vehicle_animation_sim_COMMON_INCLUDES_
#define vehicle_animation_sim_COMMON_INCLUDES_
#include <stdlib.h>
#include "rtwtypes.h"
#include "simtarget/slSimTgtSigstreamRTW.h"
#include "simtarget/slSimTgtSlioCoreRTW.h"
#include "simtarget/slSimTgtSlioClientsRTW.h"
#include "simtarget/slSimTgtSlioSdiRTW.h"
#include "sigstream_rtw.h"
#include "simstruc.h"
#include "fixedpoint.h"
#include "raccel.h"
#include "slsv_diagnostic_codegen_c_api.h"
#include "rt_logging.h"
#include "dt_info.h"
#include "ext_work.h"
#endif
#include "vehicle_animation_sim_types.h"
#include "multiword_types.h"
#include "mwmathutil.h"
#include "rt_defines.h"
#include "rtGetInf.h"
#include "rt_nonfinite.h"
#define MODEL_NAME vehicle_animation_sim
#define NSAMPLE_TIMES (4) 
#define NINPUTS (0)       
#define NOUTPUTS (0)     
#define NBLOCKIO (8) 
#define NUM_ZC_EVENTS (0) 
#ifndef NCSTATES
#define NCSTATES (4)   
#elif NCSTATES != 4
#error Invalid specification of NCSTATES defined in compiler command
#endif
#ifndef rtmGetDataMapInfo
#define rtmGetDataMapInfo(rtm) (*rt_dataMapInfoPtr)
#endif
#ifndef rtmSetDataMapInfo
#define rtmSetDataMapInfo(rtm, val) (rt_dataMapInfoPtr = &val)
#endif
#ifndef IN_RACCEL_MAIN
#endif
typedef struct { real_T kt1hy00erl [ 3 ] ; real_T k2dhhtmc1c [ 4 ] ; real_T
pmz4ikjq0y ; real_T o3ggwqepqa [ 2 ] ; real_T ok32b3uiqz [ 3 ] ; real_T
aogmtwjqau ; real_T m3cplef5sv ; real_T ao4p5sgvna ; } B ; typedef struct {
real_T jithzc3cjm [ 6 ] ; struct { void * LoggedData ; } bykjznj5yb ; } DW ;
typedef struct { real_T cu3jsrraof [ 3 ] ; real_T f0zeb2f2rh ; } X ; typedef
struct { real_T cu3jsrraof [ 3 ] ; real_T f0zeb2f2rh ; } XDot ; typedef
struct { boolean_T cu3jsrraof [ 3 ] ; boolean_T f0zeb2f2rh ; } XDis ; typedef
struct { rtwCAPI_ModelMappingInfo mmi ; } DataMapInfo ; struct P_ { real_T
PointMatrix [ 10000 ] ; real_T Integrator_IC ; real_T Gain_Gain ; real_T
Gain1_Gain ; real_T Integrator_IC_hwdznx5iyp ; real_T Speed_Value ; } ;
extern const char * RT_MEMORY_ALLOCATION_ERROR ; extern B rtB ; extern X rtX
; extern DW rtDW ; extern P rtP ; extern const rtwCAPI_ModelMappingStaticInfo
* vehicle_animation_sim_GetCAPIStaticMap ( void ) ; extern SimStruct * const
rtS ; extern const int_T gblNumToFiles ; extern const int_T gblNumFrFiles ;
extern const int_T gblNumFrWksBlocks ; extern rtInportTUtable *
gblInportTUtables ; extern const char * gblInportFileName ; extern const
int_T gblNumRootInportBlks ; extern const int_T gblNumModelInputs ; extern
const int_T gblInportDataTypeIdx [ ] ; extern const int_T gblInportDims [ ] ;
extern const int_T gblInportComplex [ ] ; extern const int_T
gblInportInterpoFlag [ ] ; extern const int_T gblInportContinuous [ ] ;
extern const int_T gblParameterTuningTid ; extern size_t gblCurrentSFcnIdx ;
extern DataMapInfo * rt_dataMapInfoPtr ; extern rtwCAPI_ModelMappingInfo *
rt_modelMapInfoPtr ; void MdlOutputs ( int_T tid ) ; void
MdlOutputsParameterSampleTime ( int_T tid ) ; void MdlUpdate ( int_T tid ) ;
void MdlTerminate ( void ) ; void MdlInitializeSizes ( void ) ; void
MdlInitializeSampleTimes ( void ) ; SimStruct * raccel_register_model ( void
) ;
#endif
