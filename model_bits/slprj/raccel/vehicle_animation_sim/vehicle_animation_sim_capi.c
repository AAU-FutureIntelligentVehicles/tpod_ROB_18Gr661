#include "__cf_vehicle_animation_sim.h"
#include "rtw_capi.h"
#ifdef HOST_CAPI_BUILD
#include "vehicle_animation_sim_capi_host.h"
#define sizeof(s) ((size_t)(0xFFFF))
#undef rt_offsetof
#define rt_offsetof(s,el) ((uint16_T)(0xFFFF))
#define TARGET_CONST
#define TARGET_STRING(s) (s)    
#else
#include "builtin_typeid_types.h"
#include "vehicle_animation_sim.h"
#include "vehicle_animation_sim_capi.h"
#include "vehicle_animation_sim_private.h"
#ifdef LIGHT_WEIGHT_CAPI
#define TARGET_CONST                  
#define TARGET_STRING(s)               (NULL)                    
#else
#define TARGET_CONST                   const
#define TARGET_STRING(s)               (s)
#endif
#endif
static const rtwCAPI_Signals rtBlockSignals [ ] = { { 0 , 1 , TARGET_STRING (
"vehicle_animation_sim/Angle Limit" ) , TARGET_STRING ( "" ) , 0 , 0 , 0 , 0
, 0 } , { 1 , 2 , TARGET_STRING ( "vehicle_animation_sim/Controller" ) ,
TARGET_STRING ( "" ) , 1 , 0 , 0 , 0 , 0 } , { 2 , 2 , TARGET_STRING (
"vehicle_animation_sim/Controller" ) , TARGET_STRING ( "" ) , 2 , 0 , 0 , 0 ,
0 } , { 3 , 0 , TARGET_STRING ( "vehicle_animation_sim/Gain1" ) ,
TARGET_STRING ( "" ) , 0 , 0 , 0 , 0 , 0 } , { 4 , 3 , TARGET_STRING (
"vehicle_animation_sim/Simple kinematic  vehicle model /MATLAB Function" ) ,
TARGET_STRING ( "" ) , 0 , 0 , 1 , 0 , 0 } , { 5 , 0 , TARGET_STRING (
"vehicle_animation_sim/Simple kinematic  vehicle model /Integrator" ) ,
TARGET_STRING ( "" ) , 0 , 0 , 1 , 0 , 0 } , { 6 , 0 , TARGET_STRING (
"vehicle_animation_sim/plot 2D planar vehicle/Rate Transition" ) ,
TARGET_STRING ( "" ) , 0 , 0 , 2 , 0 , 1 } , { 0 , 0 , ( NULL ) , ( NULL ) ,
0 , 0 , 0 , 0 , 0 } } ; static const rtwCAPI_BlockParameters
rtBlockParameters [ ] = { { 7 , TARGET_STRING ( "vehicle_animation_sim/Speed"
) , TARGET_STRING ( "Value" ) , 0 , 0 , 0 } , { 8 , TARGET_STRING (
"vehicle_animation_sim/Gain" ) , TARGET_STRING ( "Gain" ) , 0 , 0 , 0 } , { 9
, TARGET_STRING ( "vehicle_animation_sim/Gain1" ) , TARGET_STRING ( "Gain" )
, 0 , 0 , 0 } , { 10 , TARGET_STRING ( "vehicle_animation_sim/Integrator" ) ,
TARGET_STRING ( "InitialCondition" ) , 0 , 0 , 0 } , { 11 , TARGET_STRING (
"vehicle_animation_sim/Simple kinematic  vehicle model /Integrator" ) ,
TARGET_STRING ( "InitialCondition" ) , 0 , 0 , 0 } , { 0 , ( NULL ) , ( NULL
) , 0 , 0 , 0 } } ; static const rtwCAPI_ModelParameters rtModelParameters [
] = { { 12 , TARGET_STRING ( "PointMatrix" ) , 0 , 3 , 0 } , { 0 , ( NULL ) ,
0 , 0 , 0 } } ;
#ifndef HOST_CAPI_BUILD
static void * rtDataAddrMap [ ] = { & rtB . ao4p5sgvna , & rtB . aogmtwjqau ,
& rtB . m3cplef5sv , & rtB . pmz4ikjq0y , & rtB . ok32b3uiqz [ 0 ] , & rtB .
kt1hy00erl [ 0 ] , & rtB . k2dhhtmc1c [ 0 ] , & rtP . Speed_Value , & rtP .
Gain_Gain , & rtP . Gain1_Gain , & rtP . Integrator_IC_hwdznx5iyp , & rtP .
Integrator_IC , & rtP . PointMatrix [ 0 ] , } ; static int32_T *
rtVarDimsAddrMap [ ] = { ( NULL ) } ;
#endif
static TARGET_CONST rtwCAPI_DataTypeMap rtDataTypeMap [ ] = { { "double" ,
"real_T" , 0 , 0 , sizeof ( real_T ) , SS_DOUBLE , 0 , 0 } } ;
#ifdef HOST_CAPI_BUILD
#undef sizeof
#endif
static TARGET_CONST rtwCAPI_ElementMap rtElementMap [ ] = { { ( NULL ) , 0 ,
0 , 0 , 0 } , } ; static const rtwCAPI_DimensionMap rtDimensionMap [ ] = { {
rtwCAPI_SCALAR , 0 , 2 , 0 } , { rtwCAPI_VECTOR , 2 , 2 , 0 } , {
rtwCAPI_VECTOR , 4 , 2 , 0 } , { rtwCAPI_MATRIX_COL_MAJOR , 6 , 2 , 0 } } ;
static const uint_T rtDimensionArray [ ] = { 1 , 1 , 3 , 1 , 4 , 1 , 5000 , 2
} ; static const real_T rtcapiStoredFloats [ ] = { 0.0 , 0.1 } ; static const
rtwCAPI_FixPtMap rtFixPtMap [ ] = { { ( NULL ) , ( NULL ) ,
rtwCAPI_FIX_RESERVED , 0 , 0 , 0 } , } ; static const rtwCAPI_SampleTimeMap
rtSampleTimeMap [ ] = { { ( const void * ) & rtcapiStoredFloats [ 0 ] , (
const void * ) & rtcapiStoredFloats [ 0 ] , 0 , 0 } , { ( const void * ) &
rtcapiStoredFloats [ 1 ] , ( const void * ) & rtcapiStoredFloats [ 0 ] , 2 ,
0 } } ; static rtwCAPI_ModelMappingStaticInfo mmiStatic = { { rtBlockSignals
, 7 , ( NULL ) , 0 , ( NULL ) , 0 } , { rtBlockParameters , 5 ,
rtModelParameters , 1 } , { ( NULL ) , 0 } , { rtDataTypeMap , rtDimensionMap
, rtFixPtMap , rtElementMap , rtSampleTimeMap , rtDimensionArray } , "float"
, { 949491360U , 2903495935U , 155424000U , 3840311647U } , ( NULL ) , 0 , 0
} ; const rtwCAPI_ModelMappingStaticInfo *
vehicle_animation_sim_GetCAPIStaticMap ( void ) { return & mmiStatic ; }
#ifndef HOST_CAPI_BUILD
void vehicle_animation_sim_InitializeDataMapInfo ( void ) {
rtwCAPI_SetVersion ( ( * rt_dataMapInfoPtr ) . mmi , 1 ) ;
rtwCAPI_SetStaticMap ( ( * rt_dataMapInfoPtr ) . mmi , & mmiStatic ) ;
rtwCAPI_SetLoggingStaticMap ( ( * rt_dataMapInfoPtr ) . mmi , ( NULL ) ) ;
rtwCAPI_SetDataAddressMap ( ( * rt_dataMapInfoPtr ) . mmi , rtDataAddrMap ) ;
rtwCAPI_SetVarDimsAddressMap ( ( * rt_dataMapInfoPtr ) . mmi ,
rtVarDimsAddrMap ) ; rtwCAPI_SetInstanceLoggingInfo ( ( * rt_dataMapInfoPtr )
. mmi , ( NULL ) ) ; rtwCAPI_SetChildMMIArray ( ( * rt_dataMapInfoPtr ) . mmi
, ( NULL ) ) ; rtwCAPI_SetChildMMIArrayLen ( ( * rt_dataMapInfoPtr ) . mmi ,
0 ) ; }
#else
#ifdef __cplusplus
extern "C" {
#endif
void vehicle_animation_sim_host_InitializeDataMapInfo (
vehicle_animation_sim_host_DataMapInfo_T * dataMap , const char * path ) {
rtwCAPI_SetVersion ( dataMap -> mmi , 1 ) ; rtwCAPI_SetStaticMap ( dataMap ->
mmi , & mmiStatic ) ; rtwCAPI_SetDataAddressMap ( dataMap -> mmi , NULL ) ;
rtwCAPI_SetVarDimsAddressMap ( dataMap -> mmi , NULL ) ; rtwCAPI_SetPath (
dataMap -> mmi , path ) ; rtwCAPI_SetFullPath ( dataMap -> mmi , NULL ) ;
rtwCAPI_SetChildMMIArray ( dataMap -> mmi , ( NULL ) ) ;
rtwCAPI_SetChildMMIArrayLen ( dataMap -> mmi , 0 ) ; }
#ifdef __cplusplus
}
#endif
#endif
