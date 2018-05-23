# Copyright 1994-2016 The MathWorks, Inc.
#
# File    : raccel_vcx64.tmf   
#
# Abstract:
#       Template makefile for building a PC-based "rapid acceleration" 
#       executable from the generated C code for a Simulink model using
#       generated C code and the
#               Microsoft Visual C/C++ compiler version 8.0 for x64
#
#       Note that this template is automatically customized by the build 
#       procedure to create "<model>.mk"
#
#       The following defines can be used to modify the behavior of the
#       build:
#
#         OPT_OPTS       - Optimization option. See DEFAULT_OPT_OPTS in
#                          vctools.mak for default.
#         OPTS           - User specific options.
#         CPP_OPTS       - C++ compiler options.
#         USER_SRCS      - Additional user sources, such as files needed by
#                          S-functions.
#         USER_INCLUDES  - Additional include paths
#                          (i.e. USER_INCLUDES="-Iwhere-ever -Iwhere-ever2")
#
#       To enable debugging:
#         set DEBUG_BUILD = 1, which will trigger OPTS=-Zi (may vary with
#                               compiler version, see compiler doc) 
#
#       This template makefile is designed to be used with a system target
#       file that contains 'rtwgensettings.BuildDirSuffix' see raccel.tlc

#------------------------ Macros read by make_rtw -----------------------------
#
# The following macros are read by the build procedure:
#
#  MAKECMD         - This is the command used to invoke the make utility
#  HOST            - What platform this template makefile is targeted for
#                    (i.e. PC or UNIX)
#  BUILD           - Invoke make from the build procedure (yes/no)?
#  SYS_TARGET_FILE - Name of system target file.

MAKECMD         = nmake
HOST            = PC
BUILD           = yes
SYS_TARGET_FILE = raccel.tlc
BUILD_SUCCESS	= *** Created
COMPILER_TOOL_CHAIN = vcx64

#---------------------- Tokens expanded by make_rtw ---------------------------
#
# The following tokens, when wrapped with "|>" and "<|" are expanded by the
# build procedure.
#
#  MODEL_NAME          - Name of the Simulink block diagram
#  MODEL_MODULES       - Any additional generated source modules
#  MAKEFILE_NAME       - Name of makefile created from template makefile <model>.mk
#  MATLAB_ROOT         - Path to where MATLAB is installed.
#  MATLAB_BIN          - Path to MATLAB executable.
#  S_FUNCTIONS         - List of S-functions.
#  S_FUNCTIONS_LIB     - List of S-functions libraries to link.
#  BUILDARGS           - Options passed in at the command line.
#  EXT_MODE            - yes (1) or no (0): Build for external mode
#  TMW_EXTMODE_TESTING - yes (1) or no (0): Build ext_test.c for external mode
#                        testing.
#  EXTMODE_TRANSPORT   - Name of transport mechanism (e.g. tcpip, serial) for extmode
#  EXTMODE_STATIC      - yes (1) or no (0): Use static instead of dynamic mem alloc.
#  EXTMODE_STATIC_SIZE - Size of static memory allocation buffer.

MODEL                  = vehicle_animation_sim
MODULES                = rt_logging.c rtGetInf.c rtGetNaN.c rt_nonfinite.c vehicle_animation_sim_capi.c vehicle_animation_sim_data.c vehicle_animation_sim_tgtconn.c rt_logging_mmi.c rtw_modelmap_utils.c
MAKEFILE               = vehicle_animation_sim.mk
MATLAB_ROOT            = C:\Program Files\MATLAB\R2017b
ALT_MATLAB_ROOT        = C:\PROGRA~1\MATLAB\R2017b
MATLAB_BIN             = C:\Program Files\MATLAB\R2017b\bin
ALT_MATLAB_BIN         = C:\PROGRA~1\MATLAB\R2017b\bin
MASTER_ANCHOR_DIR      = 
START_DIR              = C:\Users\cuc2a\Desktop\packages_17gr561-master\model_bits
S_FUNCTIONS            = rtiostream_utils.c
S_FUNCTIONS_LIB        = $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwcoder_target_services.lib $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwcoder_ParamTuningTgtAppSvc.lib
BUILDARGS              =  ISPROTECTINGMODEL=NOTPROTECTING RSIM_SOLVER_SELECTION=2 OPTS="-DSLMSG_ALLOW_SYSTEM_ALLOC -DTGTCONN -DON_TARGET_WAIT_FOR_START=0"
RSIM_PARAMETER_LOADING = 1
ENABLE_SLEXEC_SSBRIDGE = 11
VISUAL_VER             = 15.0

EXT_MODE            = 1
TMW_EXTMODE_TESTING = 0
EXTMODE_TRANSPORT   = 0
EXTMODE_STATIC      = 0
EXTMODE_STATIC_SIZE = 1000000

SOLVER              = 
SOLVER_TYPE         = FixedStep
NUMST               = 3
TID01EQ             = 1
NCSTATES            = 4
MULTITASKING        = 0
PCMATLABROOT        = C:\\Program Files\\MATLAB\\R2017b

MODELREFS            = 
SHARED_SRC           = 
SHARED_SRC_DIR       = 
SHARED_BIN_DIR       = 
SHARED_LIB           = 
GEN_SAMPLE_MAIN      = 0

OPTIMIZATION_FLAGS   = /Od /Oy- /DNDEBUG
ADDITIONAL_LDFLAGS   = 
DEFINES_CUSTOM       = 

RACCEL_PARALLEL_EXECUTION = 0
RACCEL_PARALLEL_EXECUTION_NUM_THREADS = 2
RACCEL_NUM_PARALLEL_NODES = 0
RACCEL_PARALLEL_SIMULATOR_TYPE = 0

MODEL_HAS_DYNAMICALLY_LOADED_SFCNS = 0

# To enable debugging:
# set DEBUG_BUILD = 1
DEBUG_BUILD             = 0

#--------------------------- Model and reference models -----------------------
MODELLIB                  = vehicle_animation_simlib.lib
MODELREF_LINK_LIBS        = 
MODELREF_LINK_RSPFILE     = vehicle_animation_sim_ref.rsp
MODELREF_INC_PATH         = 
RELATIVE_PATH_TO_ANCHOR   = ..\..\..
MODELREF_TARGET_TYPE      = NONE

GLOBAL_TIMING_ENGINE       = 0

!if "$(MATLAB_ROOT)" != "$(ALT_MATLAB_ROOT)"
MATLAB_ROOT = $(ALT_MATLAB_ROOT)
!endif
!if "$(MATLAB_BIN)" != "$(ALT_MATLAB_BIN)"
MATLAB_BIN = $(ALT_MATLAB_BIN)
!endif
MATLAB_ARCH_BIN = $(MATLAB_BIN)\win64

#---------------------------Solver---------------------------------------------

RSIM_WITH_SL_SOLVER = 1

#--------------------------- Tool Specifications ------------------------------

CPU = AMD64
!include $(MATLAB_ROOT)\rtw\c\tools\vctools.mak
APPVER = 5.02

GEN_LINKER_RESPONSE  = $(MATLAB_ARCH_BIN)\createResponseFile.exe 1
CMD_FILE             = $(MODEL).rsp

#------------------------------ Include Path ----------------------------------

MATLAB_INCLUDES =                    $(MATLAB_ROOT)\simulink\include
MATLAB_INCLUDES = $(MATLAB_INCLUDES);$(MATLAB_ROOT)\extern\include
MATLAB_INCLUDES = $(MATLAB_INCLUDES);$(MATLAB_ROOT)\rtw\c\src
MATLAB_INCLUDES = $(MATLAB_INCLUDES);$(MATLAB_ROOT)\rtw\c\src\rapid
MATLAB_INCLUDES = $(MATLAB_INCLUDES);$(MATLAB_ROOT)\rtw\c\raccel
MATLAB_INCLUDES = $(MATLAB_INCLUDES);$(MATLAB_ROOT)\rtw\c\src\ext_mode\common

# Additional includes

MATLAB_INCLUDES = $(MATLAB_INCLUDES);$(START_DIR)

MATLAB_INCLUDES = $(MATLAB_INCLUDES);$(MATLAB_ROOT)\simulink\include\sf_runtime

MATLAB_INCLUDES = $(MATLAB_INCLUDES);$(START_DIR)\slprj\raccel\vehicle_animation_sim

MATLAB_INCLUDES = $(MATLAB_INCLUDES);$(MATLAB_ROOT)\toolbox\coder\rtiostream\src\utils


INCLUDE = .;$(RELATIVE_PATH_TO_ANCHOR);$(MATLAB_INCLUDES);$(INCLUDE)

!if "$(SHARED_SRC_DIR)" != ""
INCLUDE = $(INCLUDE);$(SHARED_SRC_DIR)
!endif

#------------------------ External mode ---------------------------------------
# Uncomment -DVERBOSE to have information printed to stdout
# To add a new transport layer, see the comments in
#   <matlabroot>/toolbox/simulink/simulink/extmode_transports.m

EXT_CC_OPTS = -DEXT_MODE # -DVERBOSE
!if $(EXTMODE_TRANSPORT) == 0 #tcpip
EXT_SRC = ext_svr.c updown.c ext_work.c rtiostream_interface.c rtiostream_tcpip.c
EXT_LIB = wsock32.lib
!endif
!if $(EXTMODE_TRANSPORT) == 1 #serial_win32
EXT_SRC = ext_svr.c updown.c ext_work.c ext_svr_serial_transport.c
EXT_SRC = $(EXT_SRC) ext_serial_pkt.c rtiostream_serial_interface.c rtiostream_serial.c
EXT_LIB =
!endif
!if $(TMW_EXTMODE_TESTING) == 1
EXT_SRC     = $(EXT_SRC) ext_test.c
EXT_CC_OPTS = $(EXT_CC_OPTS) -DTMW_EXTMODE_TESTING
!endif
!if $(EXTMODE_STATIC) == 1
EXT_SRC     = $(EXT_SRC) mem_mgr.c
EXT_CC_OPTS = $(EXT_CC_OPTS) -DEXTMODE_STATIC -DEXTMODE_STATIC_SIZE=$(EXTMODE_STATIC_SIZE)
!endif

#----------------------------- Parameter Tuning -------------------------------
PARAM_CC_OPTS = -DRSIM_PARAMETER_LOADING

#----------------- Compiler and Linker Options --------------------------------

# Optimization Options
OPT_OPTS = $(DEFAULT_OPT_OPTS)

# General User Options
!if "$(DEBUG_BUILD)" == "0"
DBG_FLAG =
!else
#   Set OPT_OPTS=-Zi and any additional flags for debugging
DBG_FLAG = -Zi
!endif

!if "$(OPTIMIZATION_FLAGS)" != ""
CC_OPTS = $(OPTS) $(EXT_CC_OPTS) $(OPTIMIZATION_FLAGS)
!else
CC_OPTS = $(OPT_OPTS) $(OPTS) $(EXT_CC_OPTS)
!endif


CPP_REQ_DEFINES = -DMODEL=$(MODEL) -DHAVESTDIO

CPP_REQ_DEFINES = $(CPP_REQ_DEFINES) \
                  -DNRT -DRSIM_WITH_SL_SOLVER

!if "$(ENABLE_SLEXEC_SSBRIDGE)" != "0"
CPP_REQ_DEFINES = $(CPP_REQ_DEFINES) -DENABLE_SLEXEC_SSBRIDGE=$(ENABLE_SLEXEC_SSBRIDGE)
!endif

CPP_REQ_DEFINES = $(CPP_REQ_DEFINES) -DMODEL_HAS_DYNAMICALLY_LOADED_SFCNS=$(MODEL_HAS_DYNAMICALLY_LOADED_SFCNS)

!if "$(RACCEL_PARALLEL_EXECUTION)" == "1"
CPP_REQ_DEFINES = $(CPP_REQ_DEFINES) \
		  -DRACCEL_ENABLE_PARALLEL_EXECUTION \
		  -DRACCEL_PARALLEL_EXECUTION_NUM_THREADS=$(RACCEL_PARALLEL_EXECUTION_NUM_THREADS) \
		  -DRACCEL_NUM_PARALLEL_NODES=$(RACCEL_NUM_PARALLEL_NODES) \
		  -DRACCEL_PARALLEL_SIMULATOR_TYPE=$(RACCEL_PARALLEL_SIMULATOR_TYPE)
!endif

!if "$(MULTITASKING)" == "1"
CPP_REQ_DEFINES = $(CPP_REQ_DEFINES) \
                  -DRSIM_WITH_SOLVER_MULTITASKING \
                  -DTID01EQ=$(TID01EQ) \
                  -DNUMST=$(NUMST)
!endif

# Uncomment this line to move warning level to W4
# cflags = $(cflags:W3=W4)
CFLAGS   = $(MODELREF_INC_PATH) $(cflags) $(cvarsdll) $(PARAM_CC_OPTS) /wd4996 \
	   $(DBG_FLAG) $(CC_OPTS) $(DEFINES_CUSTOM) $(CPP_REQ_DEFINES) \
	   $(USER_INCLUDES)
CPPFLAGS = $(MODELREF_INC_PATH) $(cflags) $(cvarsdll) $(PARAM_CC_OPTS) \
	   /wd4996 /EHsc- $(DBG_FLAG) $(CPP_OPTS) $(CC_OPTS) $(DEFINES_CUSTOM) \
	   $(CPP_REQ_DEFINES) $(USER_INCLUDES)
LDFLAGS  = $(ldebug) $(conflags) $(EXT_LIB) $(conlibs) $(ADDITIONAL_LDFLAGS)

#----------------------------- Source Files -----------------------------------

#Standalone executable
!if "$(MODELREF_TARGET_TYPE)" == "NONE"
PRODUCT   = $(MODEL).exe	
BUILD_PRODUCT_TYPE = executable
REQ_SRCS  = $(MODEL).c $(MODULES) $(EXT_SRC) \
            raccel_sup.c raccel_mat.c simulink_solver_api.c common_utils.c raccel_utils.c
!if "$(ENABLE_SLEXEC_SSBRIDGE)" != "0"
REQ_SRCS = $(REQ_SRCS) raccel_main_new.c
!else
REQ_SRCS = $(REQ_SRCS) raccel_main.c
!endif

!if "$(MODEL_HAS_DYNAMICALLY_LOADED_SFCNS)" == "1"
REQ_SRCS = $(REQ_SRCS) raccel_sfcn_utils.c
!endif

#Model Reference Target
!else
PRODUCT   = $(MODELLIB)
BUILD_PRODUCT_TYPE = library
REQ_SRCS  = $(MODULES)
!endif

USER_SRCS =

SRCS = $(REQ_SRCS) $(USER_SRCS) $(S_FUNCTIONS) 

OBJS_CPP_UPPER = $(SRCS:.CPP=.obj)
OBJS_CPP_LOWER = $(OBJS_CPP_UPPER:.cpp=.obj)
OBJS_C_UPPER = $(OBJS_CPP_LOWER:.C=.obj)
OBJS = $(OBJS_C_UPPER:.c=.obj)
SHARED_OBJS = $(SHARED_SRC:.c=.obj)

#--------------------------- Required Libraries -------------------------------

MAT_LIBS = $(MATLAB_ROOT)\extern\lib\win64\microsoft\libut.lib \
           $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmx.lib \
           $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmex.lib \
           $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmat.lib \
           $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwmathutil.lib \
           $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwsl_fileio.lib \
           $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwsl_services.lib \
	   $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwsigstream.lib \
	   $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwslio_core.lib \
	   $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwslio_clients.lib \
	   $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwslexec_simlog.lib

!if "$(ENABLE_SLEXEC_SSBRIDGE)" != "0"
MAT_LIBS = $(MAT_LIBS) $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwslexec_simbridge.lib
!else
MAT_LIBS = $(MAT_LIBS) $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwsl_solver_rtw.lib
!endif
!if "$(RACCEL_PARALLEL_EXECUTION)" == "1"
MAT_LIBS = $(MAT_LIBS) $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwslexec_parallel.lib
!endif
!if "$(MODEL_HAS_DYNAMICALLY_LOADED_SFCNS)" == "1"
MAT_LIBS = $(MAT_LIBS) $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwsl_sfcn_loader.lib
!endif

MAT_LIBS = $(MAT_LIBS) $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwsl_log_load_blocks.lib
MAT_LIBS = $(MAT_LIBS) $(MATLAB_ROOT)\extern\lib\win64\microsoft\libfixedpoint.lib
MAT_LIBS = $(MAT_LIBS) $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwsl_AsyncioQueue.lib
MAT_LIBS = $(MAT_LIBS) $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwsl_simtarget_instrumentation.lib
MAT_LIBS = $(MAT_LIBS) $(MATLAB_ROOT)\extern\lib\win64\microsoft\libmwsdi_raccel.lib



# ------------------------- Additional Libraries ------------------------------

LIBS =


LIBMWIPP = $(MATLAB_ROOT)\lib\win64\libmwipp.lib
LIBS = $(LIBS) $(LIBMWIPP)

#--------------------------------- Rules --------------------------------------
all: set_environment_variables $(PRODUCT)

!if "$(MODELREF_TARGET_TYPE)" == "NONE"
#--- Stand-alone model ---
$(PRODUCT) : $(OBJS) $(SHARED_LIB) $(LIBS) $(MODELREF_LINK_LIBS)
	$(GEN_LINKER_RESPONSE) $(CMD_FILE) $(OBJS)
	$(LD) $(LDFLAGS) $(S_FUNCTIONS_LIB) $(SHARED_LIB) $(MAT_LIBS) $(LIBS) \
		@$(CMD_FILE) @$(MODELREF_LINK_RSPFILE) -out:$@
	@del $(CMD_FILE)
!else
#--- Model reference Coder Target ---
$(PRODUCT) : $(OBJS) $(SHARED_LIB)
	$(GEN_LINKER_RESPONSE) $(CMD_FILE) $(OBJS)
	$(LD) -lib /OUT:$@ @$(CMD_FILE) $(S_FUNCTIONS_LIB)
!endif
	@cmd /C "echo $(BUILD_SUCCESS) $(BUILD_PRODUCT_TYPE): $@"

!if $(GEN_SAMPLE_MAIN) == 0
{$(MATLAB_ROOT)\rtw\c\raccel}.c.obj :
	$(CC) $(CFLAGS) $<
!endif

{$(MATLAB_ROOT)\rtw\c\src}.c.obj :
	$(CC) $(CFLAGS) $<

{$(MATLAB_ROOT)\rtw\c\src\rapid}.c.obj :
	$(CC) $(CFLAGS) $<

{$(MATLAB_ROOT)\rtw\c\src\ext_mode\common}.c.obj :
	$(CC) $(CFLAGS) $<

{$(MATLAB_ROOT)\rtw\c\src\rtiostream\rtiostreamtcpip}.c.obj :
	$(CC) $(CFLAGS) $<

{$(MATLAB_ROOT)\rtw\c\src\ext_mode\serial}.c.obj :
	$(CC) $(CFLAGS) $<

{$(MATLAB_ROOT)\rtw\c\src\ext_mode\custom}.c.obj :
	$(CC) $(CFLAGS) $<

simulink_solver_api.obj  : $(MATLAB_ROOT)\simulink\include\simulink_solver_api.c
	$(CC) $(CFLAGS) $(MATLAB_ROOT)\simulink\include\simulink_solver_api.c

# Additional sources

{$(MATLAB_ROOT)\rtw\c\src}.c.obj :
	$(CC) $(CFLAGS) $<

{$(MATLAB_ROOT)\simulink\src}.c.obj :
	$(CC) $(CFLAGS) $<

{$(MATLAB_ROOT)\rtw\c\src\ext_mode\common}.c.obj :
	$(CC) $(CFLAGS) $<

{$(MATLAB_ROOT)\toolbox\coder\rtiostream\src\utils}.c.obj :
	$(CC) $(CFLAGS) $<



{$(MATLAB_ROOT)\rtw\c\src}.cpp.obj :
	$(CC) $(CPPFLAGS) $<

{$(MATLAB_ROOT)\simulink\src}.cpp.obj :
	$(CC) $(CPPFLAGS) $<

{$(MATLAB_ROOT)\rtw\c\src\ext_mode\common}.cpp.obj :
	$(CC) $(CPPFLAGS) $<

{$(MATLAB_ROOT)\toolbox\coder\rtiostream\src\utils}.cpp.obj :
	$(CC) $(CPPFLAGS) $<



# Look in simulink/src helper files

{$(MATLAB_ROOT)\simulink\src}.c.obj :
	$(CC) $(CFLAGS) $<

# Put these rule last, otherwise nmake will check toolboxes first

{$(RELATIVE_PATH_TO_ANCHOR)}.cpp.obj :
	$(CC) $(CPPFLAGS) $<

.cpp.obj :
	$(CC) $(CPPFLAGS) $<

{$(RELATIVE_PATH_TO_ANCHOR)}.c.obj :
	$(CC) $(CFLAGS) $<

.c.obj :
	$(CC) $(CFLAGS) $<

!if "$(SHARED_LIB)" != ""
$(SHARED_LIB) : $(SHARED_SRC)
	@$(CC) $(CFLAGS) -Fo$(SHARED_BIN_DIR)\ @<<
$?
<<
	@$(LIBCMD) /nologo /out:$@ $(SHARED_OBJS)
!endif

set_environment_variables:
	@set INCLUDE=$(INCLUDE)
	@set LIB=$(LIB)


# Libraries:





#----------------------------- Dependencies -----------------------------------

$(OBJS) : $(MAKEFILE) rtw_proj.tmw
