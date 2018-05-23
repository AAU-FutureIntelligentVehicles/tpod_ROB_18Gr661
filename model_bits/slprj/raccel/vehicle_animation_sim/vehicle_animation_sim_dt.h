#include "__cf_vehicle_animation_sim.h"
#include "ext_types.h"
static uint_T rtDataTypeSizes [ ] = { sizeof ( real_T ) , sizeof ( real32_T )
, sizeof ( int8_T ) , sizeof ( uint8_T ) , sizeof ( int16_T ) , sizeof (
uint16_T ) , sizeof ( int32_T ) , sizeof ( uint32_T ) , sizeof ( boolean_T )
, sizeof ( fcn_call_T ) , sizeof ( int_T ) , sizeof ( pointer_T ) , sizeof (
action_T ) , 2 * sizeof ( uint32_T ) } ; static const char_T *
rtDataTypeNames [ ] = { "real_T" , "real32_T" , "int8_T" , "uint8_T" ,
"int16_T" , "uint16_T" , "int32_T" , "uint32_T" , "boolean_T" , "fcn_call_T"
, "int_T" , "pointer_T" , "action_T" , "timer_uint32_pair_T" } ; static
DataTypeTransition rtBTransitions [ ] = { { ( char_T * ) ( & rtB . kt1hy00erl
[ 0 ] ) , 0 , 0 , 16 } , { ( char_T * ) ( & rtDW . jithzc3cjm [ 0 ] ) , 0 , 0
, 6 } , { ( char_T * ) ( & rtDW . bykjznj5yb . LoggedData ) , 11 , 0 , 1 } }
; static DataTypeTransitionTable rtBTransTable = { 3U , rtBTransitions } ;
static DataTypeTransition rtPTransitions [ ] = { { ( char_T * ) ( & rtP .
PointMatrix [ 0 ] ) , 0 , 0 , 10005 } } ; static DataTypeTransitionTable
rtPTransTable = { 1U , rtPTransitions } ;
