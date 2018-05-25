#include "__cf_vehicle_animation_sim.h"
#include "rt_logging_mmi.h"
#include "vehicle_animation_sim_capi.h"
#include <math.h>
#include "vehicle_animation_sim.h"
#include "vehicle_animation_sim_private.h"
#include "vehicle_animation_sim_dt.h"
extern void * CreateDiagnosticAsVoidPtr_wrapper ( const char * id , int nargs
, ... ) ; RTWExtModeInfo * gblRTWExtModeInfo = NULL ; extern boolean_T
gblExtModeStartPktReceived ; void raccelForceExtModeShutdown ( ) { if ( !
gblExtModeStartPktReceived ) { boolean_T stopRequested = false ;
rtExtModeWaitForStartPkt ( gblRTWExtModeInfo , 3 , & stopRequested ) ; }
rtExtModeShutdown ( 3 ) ; }
#include "slsv_diagnostic_codegen_c_api.h"
const int_T gblNumToFiles = 0 ; const int_T gblNumFrFiles = 0 ; const int_T
gblNumFrWksBlocks = 0 ;
#ifdef RSIM_WITH_SOLVER_MULTITASKING
boolean_T gbl_raccel_isMultitasking = 1 ;
#else
boolean_T gbl_raccel_isMultitasking = 0 ;
#endif
boolean_T gbl_raccel_tid01eq = 1 ; int_T gbl_raccel_NumST = 4 ; const char_T
* gbl_raccel_Version = "8.13 (R2017b) 24-Jul-2017" ; void
raccel_setup_MMIStateLog ( SimStruct * S ) {
#ifdef UseMMIDataLogging
rt_FillStateSigInfoFromMMI ( ssGetRTWLogInfo ( S ) , & ssGetErrorStatus ( S )
) ;
#else
UNUSED_PARAMETER ( S ) ;
#endif
} static DataMapInfo rt_dataMapInfo ; DataMapInfo * rt_dataMapInfoPtr = &
rt_dataMapInfo ; rtwCAPI_ModelMappingInfo * rt_modelMapInfoPtr = & (
rt_dataMapInfo . mmi ) ; const char * gblSlvrJacPatternFileName =
"slprj\\raccel\\vehicle_animation_sim\\vehicle_animation_sim_Jpattern.mat" ;
const int_T gblNumRootInportBlks = 0 ; const int_T gblNumModelInputs = 0 ;
extern rtInportTUtable * gblInportTUtables ; extern const char *
gblInportFileName ; const int_T gblInportDataTypeIdx [ ] = { - 1 } ; const
int_T gblInportDims [ ] = { - 1 } ; const int_T gblInportComplex [ ] = { - 1
} ; const int_T gblInportInterpoFlag [ ] = { - 1 } ; const int_T
gblInportContinuous [ ] = { - 1 } ;
#include "simstruc.h"
#include "fixedpoint.h"
B rtB ; X rtX ; DW rtDW ; static SimStruct model_S ; SimStruct * const rtS =
& model_S ; static real_T jitqzqsjzz ( const real_T x [ 2 ] ) ; static real_T
jitqzqsjzz ( const real_T x [ 2 ] ) { real_T y ; real_T scale ; real_T absxk
; real_T t ; scale = 3.3121686421112381E-170 ; absxk = muDoubleScalarAbs ( x
[ 0 ] ) ; if ( absxk > 3.3121686421112381E-170 ) { y = 1.0 ; scale = absxk ;
} else { t = absxk / 3.3121686421112381E-170 ; y = t * t ; } absxk =
muDoubleScalarAbs ( x [ 1 ] ) ; if ( absxk > scale ) { t = scale / absxk ; y
= y * t * t + 1.0 ; scale = absxk ; } else { t = absxk / scale ; y += t * t ;
} return scale * muDoubleScalarSqrt ( y ) ; } void MdlInitialize ( void ) {
rtX . cu3jsrraof [ 0 ] = rtP . Integrator_IC ; rtX . cu3jsrraof [ 1 ] = rtP .
Integrator_IC ; rtX . cu3jsrraof [ 2 ] = rtP . Integrator_IC ; rtX .
f0zeb2f2rh = rtP . Integrator_IC_hwdznx5iyp ; } void MdlStart ( void ) { {
void * * slioCatalogueAddr = rt_slioCatalogueAddr ( ) ; void * r2 = ( NULL )
; void * * pOSigstreamManagerAddr = ( NULL ) ; const char *
errorCreatingOSigstreamManager = ( NULL ) ; const char *
errorAddingR2SharedResource = ( NULL ) ; * slioCatalogueAddr =
rtwGetNewSlioCatalogue ( rt_GetMatSigLogSelectorFileName ( ) ) ;
errorAddingR2SharedResource = rtwAddR2SharedResource (
rtwGetPointerFromUniquePtr ( rt_slioCatalogue ( ) ) , 1 ) ; if (
errorAddingR2SharedResource != ( NULL ) ) { rtwTerminateSlioCatalogue (
slioCatalogueAddr ) ; * slioCatalogueAddr = ( NULL ) ; ssSetErrorStatus ( rtS
, errorAddingR2SharedResource ) ; return ; } r2 = rtwGetR2SharedResource (
rtwGetPointerFromUniquePtr ( rt_slioCatalogue ( ) ) ) ;
pOSigstreamManagerAddr = rt_GetOSigstreamManagerAddr ( ) ;
errorCreatingOSigstreamManager = rtwOSigstreamManagerCreateInstance (
rt_GetMatSigLogSelectorFileName ( ) , r2 , pOSigstreamManagerAddr ) ; if (
errorCreatingOSigstreamManager != ( NULL ) ) { * pOSigstreamManagerAddr = (
NULL ) ; ssSetErrorStatus ( rtS , errorCreatingOSigstreamManager ) ; return ;
} } { int_T dimensions [ 1 ] = { 2 } ; rtDW . bykjznj5yb . LoggedData =
rt_CreateLogVar ( ssGetRTWLogInfo ( rtS ) , ssGetTStart ( rtS ) , ssGetTFinal
( rtS ) , 0.0 , ( & ssGetErrorStatus ( rtS ) ) , "xy" , SS_DOUBLE , 0 , 0 , 0
, 2 , 1 , dimensions , NO_LOGVALDIMS , ( NULL ) , ( NULL ) , 0 , 1 , 0.01 , 1
) ; if ( rtDW . bykjznj5yb . LoggedData == ( NULL ) ) return ; }
MdlInitialize ( ) ; { bool externalInputIsInDatasetFormat = false ; void *
pISigstreamManager = rt_GetISigstreamManager ( ) ;
rtwISigstreamManagerGetInputIsInDatasetFormat ( pISigstreamManager , &
externalInputIsInDatasetFormat ) ; if ( externalInputIsInDatasetFormat ) { }
} } void MdlOutputs ( int_T tid ) { real_T jsjvzjehif ; real_T gukrmi32le ;
real_T alpha ; real_T distance ; real_T pointVec [ 2 ] ; real_T carVec [ 2 ]
; int32_T i ; real_T b_a ; boolean_T exitg1 ; rtB . kt1hy00erl [ 0 ] = rtX .
cu3jsrraof [ 0 ] ; rtB . kt1hy00erl [ 1 ] = rtX . cu3jsrraof [ 1 ] ; rtB .
kt1hy00erl [ 2 ] = rtX . cu3jsrraof [ 2 ] ; if ( ssIsSampleHit ( rtS , 1 , 0
) ) { if ( ssGetLogOutput ( rtS ) ) { { double locTime = ssGetTaskTime ( rtS
, 1 ) ; ; if ( rtwTimeInLoggingInterval ( rtliGetLoggingInterval (
ssGetRootSS ( rtS ) -> mdlInfo -> rtwLogInfo ) , locTime ) ) {
rt_UpdateLogVar ( ( LogVar * ) ( LogVar * ) ( rtDW . bykjznj5yb . LoggedData
) , & rtB . kt1hy00erl [ 0 ] , 0 ) ; } } } } gukrmi32le = rtB . kt1hy00erl [
2 ] ; rtB . aogmtwjqau = rtP . PointMatrix [ 4999 ] ; rtB . m3cplef5sv = rtP
. PointMatrix [ 9999 ] ; alpha = 0.0 ; i = 0 ; exitg1 = false ; while ( ( !
exitg1 ) && ( i < 5000 ) ) { distance = rtP . PointMatrix [ i ] - (
muDoubleScalarCos ( gukrmi32le ) * 1.62 + rtB . kt1hy00erl [ 0 ] ) ; b_a =
rtP . PointMatrix [ 5000 + i ] - ( muDoubleScalarSin ( gukrmi32le ) * 1.62 +
rtB . kt1hy00erl [ 1 ] ) ; distance = muDoubleScalarSqrt ( distance *
distance + b_a * b_a ) ; if ( ( distance >= 3.2 ) && ( distance <= 3.6 ) ) {
pointVec [ 0 ] = ( rtP . PointMatrix [ i ] - rtB . kt1hy00erl [ 0 ] ) -
muDoubleScalarCos ( gukrmi32le ) * 1.62 ; pointVec [ 1 ] = ( rtP .
PointMatrix [ 5000 + i ] - rtB . kt1hy00erl [ 1 ] ) - muDoubleScalarSin (
gukrmi32le ) * 1.62 ; carVec [ 0 ] = muDoubleScalarCos ( gukrmi32le ) ;
carVec [ 1 ] = muDoubleScalarSin ( gukrmi32le ) ; alpha = muDoubleScalarAcos
( ( carVec [ 0 ] * pointVec [ 0 ] + carVec [ 1 ] * pointVec [ 1 ] ) / (
jitqzqsjzz ( carVec ) * jitqzqsjzz ( pointVec ) ) ) ; if ( alpha <=
0.78539816339744828 ) { rtB . aogmtwjqau = rtP . PointMatrix [ i ] ; rtB .
m3cplef5sv = rtP . PointMatrix [ 5000 + i ] ; alpha *= muDoubleScalarSign (
carVec [ 0 ] * pointVec [ 1 ] - carVec [ 1 ] * pointVec [ 0 ] ) ; exitg1 =
true ; } else { i ++ ; } } else { i ++ ; } } if ( ssIsSampleHit ( rtS , 2 , 0
) ) { } rtB . ao4p5sgvna = rtP . Gain_Gain * alpha ; if ( rtB . ao4p5sgvna >
0.50681214380594619 ) { rtB . ao4p5sgvna = 0.50681214380594619 ; } else { if
( rtB . ao4p5sgvna < - 0.50681214380594619 ) { rtB . ao4p5sgvna = -
0.50681214380594619 ; } } if ( ssIsSampleHit ( rtS , 1 , 0 ) ) { rtB .
k2dhhtmc1c [ 0 ] = rtB . kt1hy00erl [ 0 ] ; rtB . k2dhhtmc1c [ 1 ] = rtB .
kt1hy00erl [ 1 ] ; rtB . k2dhhtmc1c [ 2 ] = rtB . kt1hy00erl [ 2 ] ; rtB .
k2dhhtmc1c [ 3 ] = rtB . ao4p5sgvna ; } rtB . pmz4ikjq0y = rtP . Gain1_Gain *
alpha ; jsjvzjehif = rtX . f0zeb2f2rh ; rtB . ok32b3uiqz [ 0 ] =
muDoubleScalarCos ( rtB . kt1hy00erl [ 2 ] ) * rtP . Speed_Value ; rtB .
ok32b3uiqz [ 1 ] = muDoubleScalarSin ( rtB . kt1hy00erl [ 2 ] ) * rtP .
Speed_Value ; rtB . ok32b3uiqz [ 2 ] = muDoubleScalarTan ( rtB . ao4p5sgvna )
/ 1.64 * rtP . Speed_Value ; UNUSED_PARAMETER ( tid ) ; } void MdlUpdate (
int_T tid ) { if ( ssIsSampleHit ( rtS , 2 , 0 ) ) { } UNUSED_PARAMETER ( tid
) ; } void MdlUpdateTID3 ( int_T tid ) { UNUSED_PARAMETER ( tid ) ; } void
MdlDerivatives ( void ) { XDot * _rtXdot ; _rtXdot = ( ( XDot * ) ssGetdX (
rtS ) ) ; _rtXdot -> cu3jsrraof [ 0 ] = rtB . ok32b3uiqz [ 0 ] ; _rtXdot ->
cu3jsrraof [ 1 ] = rtB . ok32b3uiqz [ 1 ] ; _rtXdot -> cu3jsrraof [ 2 ] = rtB
. ok32b3uiqz [ 2 ] ; _rtXdot -> f0zeb2f2rh = rtB . pmz4ikjq0y ; } void
MdlProjection ( void ) { } void MdlTerminate ( void ) { if ( rt_slioCatalogue
( ) != ( NULL ) ) { void * * slioCatalogueAddr = rt_slioCatalogueAddr ( ) ;
rtwSaveDatasetsToMatFile ( rtwGetPointerFromUniquePtr ( rt_slioCatalogue ( )
) , rt_GetMatSigstreamLoggingFileName ( ) ) ; rtwTerminateSlioCatalogue (
slioCatalogueAddr ) ; * slioCatalogueAddr = NULL ; } } void
MdlInitializeSizes ( void ) { ssSetNumContStates ( rtS , 4 ) ;
ssSetNumPeriodicContStates ( rtS , 0 ) ; ssSetNumY ( rtS , 0 ) ; ssSetNumU (
rtS , 0 ) ; ssSetDirectFeedThrough ( rtS , 0 ) ; ssSetNumSampleTimes ( rtS ,
3 ) ; ssSetNumBlocks ( rtS , 20 ) ; ssSetNumBlockIO ( rtS , 8 ) ;
ssSetNumBlockParams ( rtS , 10005 ) ; } void MdlInitializeSampleTimes ( void
) { ssSetSampleTime ( rtS , 0 , 0.0 ) ; ssSetSampleTime ( rtS , 1 , 0.01 ) ;
ssSetSampleTime ( rtS , 2 , 0.1 ) ; ssSetOffsetTime ( rtS , 0 , 0.0 ) ;
ssSetOffsetTime ( rtS , 1 , 0.0 ) ; ssSetOffsetTime ( rtS , 2 , 0.0 ) ; }
void raccel_set_checksum ( ) { ssSetChecksumVal ( rtS , 0 , 949491360U ) ;
ssSetChecksumVal ( rtS , 1 , 2903495935U ) ; ssSetChecksumVal ( rtS , 2 ,
155424000U ) ; ssSetChecksumVal ( rtS , 3 , 3840311647U ) ; }
#if defined(_MSC_VER)
#pragma optimize( "", off )
#endif
SimStruct * raccel_register_model ( void ) { static struct _ssMdlInfo mdlInfo
; ( void ) memset ( ( char * ) rtS , 0 , sizeof ( SimStruct ) ) ; ( void )
memset ( ( char * ) & mdlInfo , 0 , sizeof ( struct _ssMdlInfo ) ) ;
ssSetMdlInfoPtr ( rtS , & mdlInfo ) ; { static time_T mdlPeriod [
NSAMPLE_TIMES ] ; static time_T mdlOffset [ NSAMPLE_TIMES ] ; static time_T
mdlTaskTimes [ NSAMPLE_TIMES ] ; static int_T mdlTsMap [ NSAMPLE_TIMES ] ;
static int_T mdlSampleHits [ NSAMPLE_TIMES ] ; static boolean_T
mdlTNextWasAdjustedPtr [ NSAMPLE_TIMES ] ; static int_T mdlPerTaskSampleHits
[ NSAMPLE_TIMES * NSAMPLE_TIMES ] ; static time_T mdlTimeOfNextSampleHit [
NSAMPLE_TIMES ] ; { int_T i ; for ( i = 0 ; i < NSAMPLE_TIMES ; i ++ ) {
mdlPeriod [ i ] = 0.0 ; mdlOffset [ i ] = 0.0 ; mdlTaskTimes [ i ] = 0.0 ;
mdlTsMap [ i ] = i ; mdlSampleHits [ i ] = 1 ; } } ssSetSampleTimePtr ( rtS ,
& mdlPeriod [ 0 ] ) ; ssSetOffsetTimePtr ( rtS , & mdlOffset [ 0 ] ) ;
ssSetSampleTimeTaskIDPtr ( rtS , & mdlTsMap [ 0 ] ) ; ssSetTPtr ( rtS , &
mdlTaskTimes [ 0 ] ) ; ssSetSampleHitPtr ( rtS , & mdlSampleHits [ 0 ] ) ;
ssSetTNextWasAdjustedPtr ( rtS , & mdlTNextWasAdjustedPtr [ 0 ] ) ;
ssSetPerTaskSampleHitsPtr ( rtS , & mdlPerTaskSampleHits [ 0 ] ) ;
ssSetTimeOfNextSampleHitPtr ( rtS , & mdlTimeOfNextSampleHit [ 0 ] ) ; }
ssSetSolverMode ( rtS , SOLVER_MODE_SINGLETASKING ) ; { ssSetBlockIO ( rtS ,
( ( void * ) & rtB ) ) ; ( void ) memset ( ( ( void * ) & rtB ) , 0 , sizeof
( B ) ) ; } ssSetDefaultParam ( rtS , ( real_T * ) & rtP ) ; { real_T * x = (
real_T * ) & rtX ; ssSetContStates ( rtS , x ) ; ( void ) memset ( ( void * )
x , 0 , sizeof ( X ) ) ; } { void * dwork = ( void * ) & rtDW ;
ssSetRootDWork ( rtS , dwork ) ; ( void ) memset ( dwork , 0 , sizeof ( DW )
) ; } { static DataTypeTransInfo dtInfo ; ( void ) memset ( ( char_T * ) &
dtInfo , 0 , sizeof ( dtInfo ) ) ; ssSetModelMappingInfo ( rtS , & dtInfo ) ;
dtInfo . numDataTypes = 14 ; dtInfo . dataTypeSizes = & rtDataTypeSizes [ 0 ]
; dtInfo . dataTypeNames = & rtDataTypeNames [ 0 ] ; dtInfo . BTransTable = &
rtBTransTable ; dtInfo . PTransTable = & rtPTransTable ; }
vehicle_animation_sim_InitializeDataMapInfo ( ) ;
ssSetIsRapidAcceleratorActive ( rtS , true ) ; ssSetRootSS ( rtS , rtS ) ;
ssSetVersion ( rtS , SIMSTRUCT_VERSION_LEVEL2 ) ; ssSetModelName ( rtS ,
"vehicle_animation_sim" ) ; ssSetPath ( rtS , "vehicle_animation_sim" ) ;
ssSetTStart ( rtS , 0.0 ) ; ssSetTFinal ( rtS , 45.0 ) ; ssSetStepSize ( rtS
, 0.01 ) ; ssSetFixedStepSize ( rtS , 0.01 ) ; { static RTWLogInfo
rt_DataLoggingInfo ; rt_DataLoggingInfo . loggingInterval = NULL ;
ssSetRTWLogInfo ( rtS , & rt_DataLoggingInfo ) ; } { { static int_T
rt_LoggedStateWidths [ ] = { 3 , 1 , 6 } ; static int_T
rt_LoggedStateNumDimensions [ ] = { 1 , 1 , 1 } ; static int_T
rt_LoggedStateDimensions [ ] = { 3 , 1 , 6 } ; static boolean_T
rt_LoggedStateIsVarDims [ ] = { 0 , 0 , 0 } ; static BuiltInDTypeId
rt_LoggedStateDataTypeIds [ ] = { SS_DOUBLE , SS_DOUBLE , SS_DOUBLE } ;
static int_T rt_LoggedStateComplexSignals [ ] = { 0 , 0 , 0 } ; static const
char_T * rt_LoggedStateLabels [ ] = { "CSTATE" , "CSTATE" , "DSTATE" } ;
static const char_T * rt_LoggedStateBlockNames [ ] = {
"vehicle_animation_sim/Simple kinematic \nvehicle model\n/Integrator" ,
"vehicle_animation_sim/Integrator" ,
"vehicle_animation_sim/plot 2D planar vehicle/Animation\nS-Function" } ;
static const char_T * rt_LoggedStateNames [ ] = { "" , "" , "" } ; static
boolean_T rt_LoggedStateCrossMdlRef [ ] = { 0 , 0 , 0 } ; static
RTWLogDataTypeConvert rt_RTWLogDataTypeConvert [ ] = { { 0 , SS_DOUBLE ,
SS_DOUBLE , 0 , 0 , 0 , 1.0 , 0 , 0.0 } , { 0 , SS_DOUBLE , SS_DOUBLE , 0 , 0
, 0 , 1.0 , 0 , 0.0 } , { 0 , SS_DOUBLE , SS_DOUBLE , 0 , 0 , 0 , 1.0 , 0 ,
0.0 } } ; static RTWLogSignalInfo rt_LoggedStateSignalInfo = { 3 ,
rt_LoggedStateWidths , rt_LoggedStateNumDimensions , rt_LoggedStateDimensions
, rt_LoggedStateIsVarDims , ( NULL ) , ( NULL ) , rt_LoggedStateDataTypeIds ,
rt_LoggedStateComplexSignals , ( NULL ) , ( NULL ) , { rt_LoggedStateLabels }
, ( NULL ) , ( NULL ) , ( NULL ) , { rt_LoggedStateBlockNames } , {
rt_LoggedStateNames } , rt_LoggedStateCrossMdlRef , rt_RTWLogDataTypeConvert
} ; static void * rt_LoggedStateSignalPtrs [ 3 ] ; rtliSetLogXSignalPtrs (
ssGetRTWLogInfo ( rtS ) , ( LogSignalPtrsType ) rt_LoggedStateSignalPtrs ) ;
rtliSetLogXSignalInfo ( ssGetRTWLogInfo ( rtS ) , & rt_LoggedStateSignalInfo
) ; rt_LoggedStateSignalPtrs [ 0 ] = ( void * ) & rtX . cu3jsrraof [ 0 ] ;
rt_LoggedStateSignalPtrs [ 1 ] = ( void * ) & rtX . f0zeb2f2rh ;
rt_LoggedStateSignalPtrs [ 2 ] = ( void * ) rtDW . jithzc3cjm ; } rtliSetLogT
( ssGetRTWLogInfo ( rtS ) , "tout" ) ; rtliSetLogX ( ssGetRTWLogInfo ( rtS )
, "tmp_raccel_xout" ) ; rtliSetLogXFinal ( ssGetRTWLogInfo ( rtS ) , "xFinal"
) ; rtliSetLogVarNameModifier ( ssGetRTWLogInfo ( rtS ) , "none" ) ;
rtliSetLogFormat ( ssGetRTWLogInfo ( rtS ) , 2 ) ; rtliSetLogMaxRows (
ssGetRTWLogInfo ( rtS ) , 1000 ) ; rtliSetLogDecimation ( ssGetRTWLogInfo (
rtS ) , 1 ) ; rtliSetLogY ( ssGetRTWLogInfo ( rtS ) , "" ) ;
rtliSetLogYSignalInfo ( ssGetRTWLogInfo ( rtS ) , ( NULL ) ) ;
rtliSetLogYSignalPtrs ( ssGetRTWLogInfo ( rtS ) , ( NULL ) ) ; } { static
struct _ssStatesInfo2 statesInfo2 ; ssSetStatesInfo2 ( rtS , & statesInfo2 )
; } { static ssPeriodicStatesInfo periodicStatesInfo ;
ssSetPeriodicStatesInfo ( rtS , & periodicStatesInfo ) ; } { static
ssSolverInfo slvrInfo ; static boolean_T contStatesDisabled [ 4 ] ;
ssSetSolverInfo ( rtS , & slvrInfo ) ; ssSetSolverName ( rtS , "ode3" ) ;
ssSetVariableStepSolver ( rtS , 0 ) ; ssSetSolverConsistencyChecking ( rtS ,
0 ) ; ssSetSolverAdaptiveZcDetection ( rtS , 0 ) ;
ssSetSolverRobustResetMethod ( rtS , 0 ) ; ssSetSolverStateProjection ( rtS ,
0 ) ; ssSetSolverMassMatrixType ( rtS , ( ssMatrixType ) 0 ) ;
ssSetSolverMassMatrixNzMax ( rtS , 0 ) ; ssSetModelOutputs ( rtS , MdlOutputs
) ; ssSetModelLogData ( rtS , rt_UpdateTXYLogVars ) ;
ssSetModelLogDataIfInInterval ( rtS , rt_UpdateTXXFYLogVars ) ;
ssSetModelUpdate ( rtS , MdlUpdate ) ; ssSetModelDerivatives ( rtS ,
MdlDerivatives ) ; ssSetTNextTid ( rtS , INT_MIN ) ; ssSetTNext ( rtS ,
rtMinusInf ) ; ssSetSolverNeedsReset ( rtS ) ; ssSetNumNonsampledZCs ( rtS ,
0 ) ; ssSetContStateDisabled ( rtS , contStatesDisabled ) ; }
ssSetChecksumVal ( rtS , 0 , 949491360U ) ; ssSetChecksumVal ( rtS , 1 ,
2903495935U ) ; ssSetChecksumVal ( rtS , 2 , 155424000U ) ; ssSetChecksumVal
( rtS , 3 , 3840311647U ) ; { static const sysRanDType rtAlwaysEnabled =
SUBSYS_RAN_BC_ENABLE ; static RTWExtModeInfo rt_ExtModeInfo ; static const
sysRanDType * systemRan [ 5 ] ; gblRTWExtModeInfo = & rt_ExtModeInfo ;
ssSetRTWExtModeInfo ( rtS , & rt_ExtModeInfo ) ;
rteiSetSubSystemActiveVectorAddresses ( & rt_ExtModeInfo , systemRan ) ;
systemRan [ 0 ] = & rtAlwaysEnabled ; systemRan [ 1 ] = & rtAlwaysEnabled ;
systemRan [ 2 ] = & rtAlwaysEnabled ; systemRan [ 3 ] = & rtAlwaysEnabled ;
systemRan [ 4 ] = & rtAlwaysEnabled ; rteiSetModelMappingInfoPtr (
ssGetRTWExtModeInfo ( rtS ) , & ssGetModelMappingInfo ( rtS ) ) ;
rteiSetChecksumsPtr ( ssGetRTWExtModeInfo ( rtS ) , ssGetChecksums ( rtS ) )
; rteiSetTPtr ( ssGetRTWExtModeInfo ( rtS ) , ssGetTPtr ( rtS ) ) ; } return
rtS ; }
#if defined(_MSC_VER)
#pragma optimize( "", on )
#endif
const int_T gblParameterTuningTid = 3 ; void MdlOutputsParameterSampleTime (
int_T tid ) { UNUSED_PARAMETER ( tid ) ; }
