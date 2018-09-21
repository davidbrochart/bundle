############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2016 Xilinx, Inc. All Rights Reserved.
############################################################
open_project ddr2fpga
set_top ddr2fpga
add_files cpp/ddr2fpga.cpp
add_files -tb cpp/test_ddr2fpga.cpp
open_solution "solution1"
set_part {xc7z020clg400-1} -tool vivado
create_clock -period 10 -name default
#source "./ddr2fpga/solution1/directives.tcl"
csim_design
csynth_design
cosim_design
export_design -format ip_catalog
