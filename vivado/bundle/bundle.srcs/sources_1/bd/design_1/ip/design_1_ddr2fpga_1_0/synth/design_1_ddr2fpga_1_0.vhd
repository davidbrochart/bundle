-- (c) Copyright 1995-2018 Xilinx, Inc. All rights reserved.
-- 
-- This file contains confidential and proprietary information
-- of Xilinx, Inc. and is protected under U.S. and
-- international copyright and other intellectual property
-- laws.
-- 
-- DISCLAIMER
-- This disclaimer is not a license and does not grant any
-- rights to the materials distributed herewith. Except as
-- otherwise provided in a valid license issued to you by
-- Xilinx, and to the maximum extent permitted by applicable
-- law: (1) THESE MATERIALS ARE MADE AVAILABLE "AS IS" AND
-- WITH ALL FAULTS, AND XILINX HEREBY DISCLAIMS ALL WARRANTIES
-- AND CONDITIONS, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING
-- BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, NON-
-- INFRINGEMENT, OR FITNESS FOR ANY PARTICULAR PURPOSE; and
-- (2) Xilinx shall not be liable (whether in contract or tort,
-- including negligence, or under any other theory of
-- liability) for any loss or damage of any kind or nature
-- related to, arising under or in connection with these
-- materials, including for any direct, or any indirect,
-- special, incidental, or consequential loss or damage
-- (including loss of data, profits, goodwill, or any type of
-- loss or damage suffered as a result of any action brought
-- by a third party) even if such damage or loss was
-- reasonably foreseeable or Xilinx had been advised of the
-- possibility of the same.
-- 
-- CRITICAL APPLICATIONS
-- Xilinx products are not designed or intended to be fail-
-- safe, or for use in any application requiring fail-safe
-- performance, such as life-support or safety devices or
-- systems, Class III medical devices, nuclear facilities,
-- applications related to the deployment of airbags, or any
-- other applications that could lead to death, personal
-- injury, or severe property or environmental damage
-- (individually and collectively, "Critical
-- Applications"). Customer assumes the sole risk and
-- liability of any use of Xilinx products in Critical
-- Applications, subject only to applicable laws and
-- regulations governing limitations on product liability.
-- 
-- THIS COPYRIGHT NOTICE AND DISCLAIMER MUST BE RETAINED AS
-- PART OF THIS FILE AT ALL TIMES.
-- 
-- DO NOT MODIFY THIS FILE.

-- IP VLNV: xilinx.com:hls:ddr2fpga:1.0
-- IP Revision: 1809241118

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
use work.bundlepack.all;

ENTITY design_1_ddr2fpga_1_0 IS
  PORT (
    o_mem_i : out STD_LOGIC_VECTOR (MEM_BITNB - 1 downto 0);
    mem_V_ce0 : OUT STD_LOGIC;
    mem_V_we0 : OUT STD_LOGIC;
    s_axi_ctrl_AWADDR : IN STD_LOGIC_VECTOR(4 DOWNTO 0);
    s_axi_ctrl_AWVALID : IN STD_LOGIC;
    s_axi_ctrl_AWREADY : OUT STD_LOGIC;
    s_axi_ctrl_WDATA : IN STD_LOGIC_VECTOR(31 DOWNTO 0);
    s_axi_ctrl_WSTRB : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
    s_axi_ctrl_WVALID : IN STD_LOGIC;
    s_axi_ctrl_WREADY : OUT STD_LOGIC;
    s_axi_ctrl_BRESP : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
    s_axi_ctrl_BVALID : OUT STD_LOGIC;
    s_axi_ctrl_BREADY : IN STD_LOGIC;
    s_axi_ctrl_ARADDR : IN STD_LOGIC_VECTOR(4 DOWNTO 0);
    s_axi_ctrl_ARVALID : IN STD_LOGIC;
    s_axi_ctrl_ARREADY : OUT STD_LOGIC;
    s_axi_ctrl_RDATA : OUT STD_LOGIC_VECTOR(31 DOWNTO 0);
    s_axi_ctrl_RRESP : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
    s_axi_ctrl_RVALID : OUT STD_LOGIC;
    s_axi_ctrl_RREADY : IN STD_LOGIC;
    ap_clk : IN STD_LOGIC;
    ap_rst_n : IN STD_LOGIC;
    interrupt : OUT STD_LOGIC;
    i_stream_TVALID : IN STD_LOGIC;
    i_stream_TREADY : OUT STD_LOGIC;
    i_stream_TDATA : IN STD_LOGIC_VECTOR(63 DOWNTO 0);
    i_stream_TDEST : IN STD_LOGIC_VECTOR(0 DOWNTO 0);
    i_stream_TKEEP : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
    i_stream_TSTRB : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
    i_stream_TUSER : IN STD_LOGIC_VECTOR(0 DOWNTO 0);
    i_stream_TLAST : IN STD_LOGIC_VECTOR(0 DOWNTO 0);
    i_stream_TID : IN STD_LOGIC_VECTOR(0 DOWNTO 0);
    mem_V_address0 : OUT STD_LOGIC_VECTOR(MEM_DEPTH_BITNB - 1 DOWNTO 0);
    mem_V_d0 : OUT STD_LOGIC_VECTOR(MEM_WIDTH - 1 DOWNTO 0)
  );
END design_1_ddr2fpga_1_0;

ARCHITECTURE design_1_ddr2fpga_1_0_arch OF design_1_ddr2fpga_1_0 IS
  ATTRIBUTE DowngradeIPIdentifiedWarnings : STRING;
  ATTRIBUTE DowngradeIPIdentifiedWarnings OF design_1_ddr2fpga_1_0_arch: ARCHITECTURE IS "yes";
  COMPONENT ddr2fpga IS
    GENERIC (
      C_S_AXI_CTRL_ADDR_WIDTH : INTEGER;
      C_S_AXI_CTRL_DATA_WIDTH : INTEGER
    );
    PORT (
      o_mem_i : out STD_LOGIC_VECTOR (MEM_BITNB - 1 downto 0);
      mem_V_ce0 : OUT STD_LOGIC;
      mem_V_we0 : OUT STD_LOGIC;
      s_axi_ctrl_AWADDR : IN STD_LOGIC_VECTOR(4 DOWNTO 0);
      s_axi_ctrl_AWVALID : IN STD_LOGIC;
      s_axi_ctrl_AWREADY : OUT STD_LOGIC;
      s_axi_ctrl_WDATA : IN STD_LOGIC_VECTOR(31 DOWNTO 0);
      s_axi_ctrl_WSTRB : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
      s_axi_ctrl_WVALID : IN STD_LOGIC;
      s_axi_ctrl_WREADY : OUT STD_LOGIC;
      s_axi_ctrl_BRESP : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
      s_axi_ctrl_BVALID : OUT STD_LOGIC;
      s_axi_ctrl_BREADY : IN STD_LOGIC;
      s_axi_ctrl_ARADDR : IN STD_LOGIC_VECTOR(4 DOWNTO 0);
      s_axi_ctrl_ARVALID : IN STD_LOGIC;
      s_axi_ctrl_ARREADY : OUT STD_LOGIC;
      s_axi_ctrl_RDATA : OUT STD_LOGIC_VECTOR(31 DOWNTO 0);
      s_axi_ctrl_RRESP : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
      s_axi_ctrl_RVALID : OUT STD_LOGIC;
      s_axi_ctrl_RREADY : IN STD_LOGIC;
      ap_clk : IN STD_LOGIC;
      ap_rst_n : IN STD_LOGIC;
      interrupt : OUT STD_LOGIC;
      i_stream_TVALID : IN STD_LOGIC;
      i_stream_TREADY : OUT STD_LOGIC;
      i_stream_TDATA : IN STD_LOGIC_VECTOR(63 DOWNTO 0);
      i_stream_TDEST : IN STD_LOGIC_VECTOR(0 DOWNTO 0);
      i_stream_TKEEP : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
      i_stream_TSTRB : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
      i_stream_TUSER : IN STD_LOGIC_VECTOR(0 DOWNTO 0);
      i_stream_TLAST : IN STD_LOGIC_VECTOR(0 DOWNTO 0);
      i_stream_TID : IN STD_LOGIC_VECTOR(0 DOWNTO 0);
      mem_V_address0 : OUT STD_LOGIC_VECTOR(MEM_DEPTH_BITNB - 1 DOWNTO 0);
      mem_V_d0 : OUT STD_LOGIC_VECTOR(MEM_WIDTH - 1 DOWNTO 0)
    );
  END COMPONENT ddr2fpga;
  ATTRIBUTE X_CORE_INFO : STRING;
  ATTRIBUTE X_CORE_INFO OF design_1_ddr2fpga_1_0_arch: ARCHITECTURE IS "ddr2fpga,Vivado 2016.1";
  ATTRIBUTE CHECK_LICENSE_TYPE : STRING;
  ATTRIBUTE CHECK_LICENSE_TYPE OF design_1_ddr2fpga_1_0_arch : ARCHITECTURE IS "design_1_ddr2fpga_1_0,ddr2fpga,{}";
  ATTRIBUTE CORE_GENERATION_INFO : STRING;
  ATTRIBUTE CORE_GENERATION_INFO OF design_1_ddr2fpga_1_0_arch: ARCHITECTURE IS "design_1_ddr2fpga_1_0,ddr2fpga,{x_ipProduct=Vivado 2016.1,x_ipVendor=xilinx.com,x_ipLibrary=hls,x_ipName=ddr2fpga,x_ipVersion=1.0,x_ipCoreRevision=1809241118,x_ipLanguage=VHDL,x_ipSimLanguage=MIXED,C_S_AXI_CTRL_ADDR_WIDTH=5,C_S_AXI_CTRL_DATA_WIDTH=32}";
  ATTRIBUTE X_INTERFACE_INFO : STRING;
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_AWADDR: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl AWADDR";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_AWVALID: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl AWVALID";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_AWREADY: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl AWREADY";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_WDATA: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl WDATA";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_WSTRB: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl WSTRB";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_WVALID: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl WVALID";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_WREADY: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl WREADY";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_BRESP: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl BRESP";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_BVALID: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl BVALID";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_BREADY: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl BREADY";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_ARADDR: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl ARADDR";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_ARVALID: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl ARVALID";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_ARREADY: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl ARREADY";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_RDATA: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl RDATA";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_RRESP: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl RRESP";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_RVALID: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl RVALID";
  ATTRIBUTE X_INTERFACE_INFO OF s_axi_ctrl_RREADY: SIGNAL IS "xilinx.com:interface:aximm:1.0 s_axi_ctrl RREADY";
  ATTRIBUTE X_INTERFACE_INFO OF ap_clk: SIGNAL IS "xilinx.com:signal:clock:1.0 ap_clk CLK";
  ATTRIBUTE X_INTERFACE_INFO OF ap_rst_n: SIGNAL IS "xilinx.com:signal:reset:1.0 ap_rst_n RST";
  ATTRIBUTE X_INTERFACE_INFO OF interrupt: SIGNAL IS "xilinx.com:signal:interrupt:1.0 interrupt INTERRUPT";
  ATTRIBUTE X_INTERFACE_INFO OF i_stream_TVALID: SIGNAL IS "xilinx.com:interface:axis:1.0 i_stream TVALID";
  ATTRIBUTE X_INTERFACE_INFO OF i_stream_TREADY: SIGNAL IS "xilinx.com:interface:axis:1.0 i_stream TREADY";
  ATTRIBUTE X_INTERFACE_INFO OF i_stream_TDATA: SIGNAL IS "xilinx.com:interface:axis:1.0 i_stream TDATA";
  ATTRIBUTE X_INTERFACE_INFO OF i_stream_TDEST: SIGNAL IS "xilinx.com:interface:axis:1.0 i_stream TDEST";
  ATTRIBUTE X_INTERFACE_INFO OF i_stream_TKEEP: SIGNAL IS "xilinx.com:interface:axis:1.0 i_stream TKEEP";
  ATTRIBUTE X_INTERFACE_INFO OF i_stream_TSTRB: SIGNAL IS "xilinx.com:interface:axis:1.0 i_stream TSTRB";
  ATTRIBUTE X_INTERFACE_INFO OF i_stream_TUSER: SIGNAL IS "xilinx.com:interface:axis:1.0 i_stream TUSER";
  ATTRIBUTE X_INTERFACE_INFO OF i_stream_TLAST: SIGNAL IS "xilinx.com:interface:axis:1.0 i_stream TLAST";
  ATTRIBUTE X_INTERFACE_INFO OF i_stream_TID: SIGNAL IS "xilinx.com:interface:axis:1.0 i_stream TID";
  ATTRIBUTE X_INTERFACE_INFO OF mem_V_address0: SIGNAL IS "xilinx.com:signal:data:1.0 mem_V_address0 DATA";
  ATTRIBUTE X_INTERFACE_INFO OF mem_V_d0: SIGNAL IS "xilinx.com:signal:data:1.0 mem_V_d0 DATA";
BEGIN
  U0 : ddr2fpga
    GENERIC MAP (
      C_S_AXI_CTRL_ADDR_WIDTH => 5,
      C_S_AXI_CTRL_DATA_WIDTH => 32
    )
    PORT MAP (
      o_mem_i => o_mem_i,
      mem_V_ce0 => mem_V_ce0,
      mem_V_we0 => mem_V_we0,
      s_axi_ctrl_AWADDR => s_axi_ctrl_AWADDR,
      s_axi_ctrl_AWVALID => s_axi_ctrl_AWVALID,
      s_axi_ctrl_AWREADY => s_axi_ctrl_AWREADY,
      s_axi_ctrl_WDATA => s_axi_ctrl_WDATA,
      s_axi_ctrl_WSTRB => s_axi_ctrl_WSTRB,
      s_axi_ctrl_WVALID => s_axi_ctrl_WVALID,
      s_axi_ctrl_WREADY => s_axi_ctrl_WREADY,
      s_axi_ctrl_BRESP => s_axi_ctrl_BRESP,
      s_axi_ctrl_BVALID => s_axi_ctrl_BVALID,
      s_axi_ctrl_BREADY => s_axi_ctrl_BREADY,
      s_axi_ctrl_ARADDR => s_axi_ctrl_ARADDR,
      s_axi_ctrl_ARVALID => s_axi_ctrl_ARVALID,
      s_axi_ctrl_ARREADY => s_axi_ctrl_ARREADY,
      s_axi_ctrl_RDATA => s_axi_ctrl_RDATA,
      s_axi_ctrl_RRESP => s_axi_ctrl_RRESP,
      s_axi_ctrl_RVALID => s_axi_ctrl_RVALID,
      s_axi_ctrl_RREADY => s_axi_ctrl_RREADY,
      ap_clk => ap_clk,
      ap_rst_n => ap_rst_n,
      interrupt => interrupt,
      i_stream_TVALID => i_stream_TVALID,
      i_stream_TREADY => i_stream_TREADY,
      i_stream_TDATA => i_stream_TDATA,
      i_stream_TDEST => i_stream_TDEST,
      i_stream_TKEEP => i_stream_TKEEP,
      i_stream_TSTRB => i_stream_TSTRB,
      i_stream_TUSER => i_stream_TUSER,
      i_stream_TLAST => i_stream_TLAST,
      i_stream_TID => i_stream_TID,
      mem_V_address0 => mem_V_address0,
      mem_V_d0 => mem_V_d0
    );
END design_1_ddr2fpga_1_0_arch;
