############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2016 Xilinx, Inc. All Rights Reserved.
############################################################
open_project crossbar
set_top crossbar
add_files cpp/crossbar.cpp
open_solution "solution1"
set_part {xc7z020clg400-1} -tool vivado
create_clock -period 10 -name default
#source "./crossbar/solution1/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -format ip_catalog
