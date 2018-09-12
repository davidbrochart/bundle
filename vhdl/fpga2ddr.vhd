-- ==============================================================
-- RTL generated by Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC
-- Version: 2016.1
-- Copyright (C) 1986-2016 Xilinx, Inc. All Rights Reserved.
-- 
-- ===========================================================

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity fpga2ddr is
generic (
    C_S_AXI_CTRL_ADDR_WIDTH : INTEGER := 5;
    C_S_AXI_CTRL_DATA_WIDTH : INTEGER := 32 );
port (
    ap_clk : IN STD_LOGIC;
    ap_rst_n : IN STD_LOGIC;
    o_stream_TDATA : OUT STD_LOGIC_VECTOR (63 downto 0);
    o_stream_TVALID : OUT STD_LOGIC;
    o_stream_TREADY : IN STD_LOGIC;
    o_stream_TKEEP : OUT STD_LOGIC_VECTOR (7 downto 0);
    o_stream_TSTRB : OUT STD_LOGIC_VECTOR (7 downto 0);
    o_stream_TUSER : OUT STD_LOGIC_VECTOR (0 downto 0);
    o_stream_TLAST : OUT STD_LOGIC_VECTOR (0 downto 0);
    o_stream_TID : OUT STD_LOGIC_VECTOR (0 downto 0);
    o_stream_TDEST : OUT STD_LOGIC_VECTOR (0 downto 0);
    mem_V_address0 : OUT STD_LOGIC_VECTOR (9 downto 0);
    mem_V_ce0 : OUT STD_LOGIC;
    mem_V_q0 : IN STD_LOGIC_VECTOR (63 downto 0);
    s_axi_ctrl_AWVALID : IN STD_LOGIC;
    s_axi_ctrl_AWREADY : OUT STD_LOGIC;
    s_axi_ctrl_AWADDR : IN STD_LOGIC_VECTOR (C_S_AXI_CTRL_ADDR_WIDTH-1 downto 0);
    s_axi_ctrl_WVALID : IN STD_LOGIC;
    s_axi_ctrl_WREADY : OUT STD_LOGIC;
    s_axi_ctrl_WDATA : IN STD_LOGIC_VECTOR (C_S_AXI_CTRL_DATA_WIDTH-1 downto 0);
    s_axi_ctrl_WSTRB : IN STD_LOGIC_VECTOR (C_S_AXI_CTRL_DATA_WIDTH/8-1 downto 0);
    s_axi_ctrl_ARVALID : IN STD_LOGIC;
    s_axi_ctrl_ARREADY : OUT STD_LOGIC;
    s_axi_ctrl_ARADDR : IN STD_LOGIC_VECTOR (C_S_AXI_CTRL_ADDR_WIDTH-1 downto 0);
    s_axi_ctrl_RVALID : OUT STD_LOGIC;
    s_axi_ctrl_RREADY : IN STD_LOGIC;
    s_axi_ctrl_RDATA : OUT STD_LOGIC_VECTOR (C_S_AXI_CTRL_DATA_WIDTH-1 downto 0);
    s_axi_ctrl_RRESP : OUT STD_LOGIC_VECTOR (1 downto 0);
    s_axi_ctrl_BVALID : OUT STD_LOGIC;
    s_axi_ctrl_BREADY : IN STD_LOGIC;
    s_axi_ctrl_BRESP : OUT STD_LOGIC_VECTOR (1 downto 0);
    interrupt : OUT STD_LOGIC );
end;


architecture behav of fpga2ddr is 
    attribute CORE_GENERATION_INFO : STRING;
    attribute CORE_GENERATION_INFO of behav : architecture is
    "fpga2ddr,hls_ip_2016_1,{HLS_INPUT_TYPE=cxx,HLS_INPUT_FLOAT=0,HLS_INPUT_FIXED=1,HLS_INPUT_PART=xc7z020clg400-1,HLS_INPUT_CLOCK=10.000000,HLS_INPUT_ARCH=others,HLS_SYN_CLOCK=2.840000,HLS_SYN_LAT=-1,HLS_SYN_TPT=none,HLS_SYN_MEM=0,HLS_SYN_DSP=0,HLS_SYN_FF=111,HLS_SYN_LUT=116}";
    constant ap_const_logic_1 : STD_LOGIC := '1';
    constant ap_const_logic_0 : STD_LOGIC := '0';
    constant ap_ST_st1_fsm_0 : STD_LOGIC_VECTOR (2 downto 0) := "001";
    constant ap_ST_st2_fsm_1 : STD_LOGIC_VECTOR (2 downto 0) := "010";
    constant ap_ST_st3_fsm_2 : STD_LOGIC_VECTOR (2 downto 0) := "100";
    constant ap_const_lv32_0 : STD_LOGIC_VECTOR (31 downto 0) := "00000000000000000000000000000000";
    constant ap_const_lv1_1 : STD_LOGIC_VECTOR (0 downto 0) := "1";
    constant ap_const_lv32_2 : STD_LOGIC_VECTOR (31 downto 0) := "00000000000000000000000000000010";
    constant C_S_AXI_DATA_WIDTH : INTEGER range 63 downto 0 := 20;
    constant ap_const_lv32_1 : STD_LOGIC_VECTOR (31 downto 0) := "00000000000000000000000000000001";
    constant ap_const_lv1_0 : STD_LOGIC_VECTOR (0 downto 0) := "0";
    constant ap_const_lv9_0 : STD_LOGIC_VECTOR (8 downto 0) := "000000000";
    constant ap_const_lv8_7 : STD_LOGIC_VECTOR (7 downto 0) := "00000111";
    constant ap_const_lv12_FFF : STD_LOGIC_VECTOR (11 downto 0) := "111111111111";
    constant ap_const_lv9_1 : STD_LOGIC_VECTOR (8 downto 0) := "000000001";

    signal ap_rst_n_inv : STD_LOGIC;
    signal ap_start : STD_LOGIC;
    signal ap_done : STD_LOGIC;
    signal ap_idle : STD_LOGIC;
    signal ap_CS_fsm : STD_LOGIC_VECTOR (2 downto 0) := "001";
    attribute fsm_encoding : string;
    attribute fsm_encoding of ap_CS_fsm : signal is "none";
    signal ap_sig_cseq_ST_st1_fsm_0 : STD_LOGIC;
    signal ap_sig_20 : BOOLEAN;
    signal ap_ready : STD_LOGIC;
    signal mem_i_V : STD_LOGIC_VECTOR (5 downto 0);
    signal data_nb_V : STD_LOGIC_VECTOR (10 downto 0);
    signal o_stream_TDATA_blk_n : STD_LOGIC;
    signal ap_sig_cseq_ST_st3_fsm_2 : STD_LOGIC;
    signal ap_sig_50 : BOOLEAN;
    signal data_nb_V_read_reg_153 : STD_LOGIC_VECTOR (10 downto 0);
    signal r_V_fu_118_p2 : STD_LOGIC_VECTOR (11 downto 0);
    signal r_V_reg_158 : STD_LOGIC_VECTOR (11 downto 0);
    signal i_V_fu_133_p2 : STD_LOGIC_VECTOR (8 downto 0);
    signal i_V_reg_166 : STD_LOGIC_VECTOR (8 downto 0);
    signal ap_sig_cseq_ST_st2_fsm_1 : STD_LOGIC;
    signal ap_sig_102 : BOOLEAN;
    signal tmp_2_fu_128_p2 : STD_LOGIC_VECTOR (0 downto 0);
    signal r_ostream_last_V_fu_148_p2 : STD_LOGIC_VECTOR (0 downto 0);
    signal r_ostream_last_V_reg_176 : STD_LOGIC_VECTOR (0 downto 0);
    signal p_s_reg_103 : STD_LOGIC_VECTOR (8 downto 0);
    signal ap_sig_ioackin_o_stream_TREADY : STD_LOGIC;
    signal tmp_3_fu_139_p1 : STD_LOGIC_VECTOR (63 downto 0);
    signal ap_reg_ioackin_o_stream_TREADY : STD_LOGIC := '0';
    signal lhs_V_cast_fu_114_p1 : STD_LOGIC_VECTOR (11 downto 0);
    signal tmp_cast_fu_124_p1 : STD_LOGIC_VECTOR (10 downto 0);
    signal tmp_6_cast_fu_144_p1 : STD_LOGIC_VECTOR (11 downto 0);
    signal ap_NS_fsm : STD_LOGIC_VECTOR (2 downto 0);

    component fpga2ddr_ctrl_s_axi IS
    generic (
        C_S_AXI_ADDR_WIDTH : INTEGER;
        C_S_AXI_DATA_WIDTH : INTEGER );
    port (
        AWVALID : IN STD_LOGIC;
        AWREADY : OUT STD_LOGIC;
        AWADDR : IN STD_LOGIC_VECTOR (C_S_AXI_ADDR_WIDTH-1 downto 0);
        WVALID : IN STD_LOGIC;
        WREADY : OUT STD_LOGIC;
        WDATA : IN STD_LOGIC_VECTOR (C_S_AXI_DATA_WIDTH-1 downto 0);
        WSTRB : IN STD_LOGIC_VECTOR (C_S_AXI_DATA_WIDTH/8-1 downto 0);
        ARVALID : IN STD_LOGIC;
        ARREADY : OUT STD_LOGIC;
        ARADDR : IN STD_LOGIC_VECTOR (C_S_AXI_ADDR_WIDTH-1 downto 0);
        RVALID : OUT STD_LOGIC;
        RREADY : IN STD_LOGIC;
        RDATA : OUT STD_LOGIC_VECTOR (C_S_AXI_DATA_WIDTH-1 downto 0);
        RRESP : OUT STD_LOGIC_VECTOR (1 downto 0);
        BVALID : OUT STD_LOGIC;
        BREADY : IN STD_LOGIC;
        BRESP : OUT STD_LOGIC_VECTOR (1 downto 0);
        ACLK : IN STD_LOGIC;
        ARESET : IN STD_LOGIC;
        ACLK_EN : IN STD_LOGIC;
        ap_start : OUT STD_LOGIC;
        interrupt : OUT STD_LOGIC;
        ap_ready : IN STD_LOGIC;
        ap_done : IN STD_LOGIC;
        ap_idle : IN STD_LOGIC;
        mem_i_V : OUT STD_LOGIC_VECTOR (5 downto 0);
        data_nb_V : OUT STD_LOGIC_VECTOR (10 downto 0) );
    end component;



begin
    fpga2ddr_ctrl_s_axi_U : component fpga2ddr_ctrl_s_axi
    generic map (
        C_S_AXI_ADDR_WIDTH => C_S_AXI_CTRL_ADDR_WIDTH,
        C_S_AXI_DATA_WIDTH => C_S_AXI_CTRL_DATA_WIDTH)
    port map (
        AWVALID => s_axi_ctrl_AWVALID,
        AWREADY => s_axi_ctrl_AWREADY,
        AWADDR => s_axi_ctrl_AWADDR,
        WVALID => s_axi_ctrl_WVALID,
        WREADY => s_axi_ctrl_WREADY,
        WDATA => s_axi_ctrl_WDATA,
        WSTRB => s_axi_ctrl_WSTRB,
        ARVALID => s_axi_ctrl_ARVALID,
        ARREADY => s_axi_ctrl_ARREADY,
        ARADDR => s_axi_ctrl_ARADDR,
        RVALID => s_axi_ctrl_RVALID,
        RREADY => s_axi_ctrl_RREADY,
        RDATA => s_axi_ctrl_RDATA,
        RRESP => s_axi_ctrl_RRESP,
        BVALID => s_axi_ctrl_BVALID,
        BREADY => s_axi_ctrl_BREADY,
        BRESP => s_axi_ctrl_BRESP,
        ACLK => ap_clk,
        ARESET => ap_rst_n_inv,
        ACLK_EN => ap_const_logic_1,
        ap_start => ap_start,
        interrupt => interrupt,
        ap_ready => ap_ready,
        ap_done => ap_done,
        ap_idle => ap_idle,
        mem_i_V => mem_i_V,
        data_nb_V => data_nb_V);





    ap_CS_fsm_assign_proc : process(ap_clk)
    begin
        if (ap_clk'event and ap_clk =  '1') then
            if (ap_rst_n_inv = '1') then
                ap_CS_fsm <= ap_ST_st1_fsm_0;
            else
                ap_CS_fsm <= ap_NS_fsm;
            end if;
        end if;
    end process;


    ap_reg_ioackin_o_stream_TREADY_assign_proc : process(ap_clk)
    begin
        if (ap_clk'event and ap_clk =  '1') then
            if (ap_rst_n_inv = '1') then
                ap_reg_ioackin_o_stream_TREADY <= ap_const_logic_0;
            else
                if ((((ap_const_logic_1 = ap_sig_cseq_ST_st3_fsm_2) and not((ap_const_logic_0 = ap_sig_ioackin_o_stream_TREADY))))) then 
                    ap_reg_ioackin_o_stream_TREADY <= ap_const_logic_0;
                elsif ((((ap_const_logic_1 = ap_sig_cseq_ST_st3_fsm_2) and (ap_const_logic_1 = o_stream_TREADY)))) then 
                    ap_reg_ioackin_o_stream_TREADY <= ap_const_logic_1;
                end if; 
            end if;
        end if;
    end process;


    p_s_reg_103_assign_proc : process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if (((ap_const_logic_1 = ap_sig_cseq_ST_st3_fsm_2) and not((ap_const_logic_0 = ap_sig_ioackin_o_stream_TREADY)))) then 
                p_s_reg_103 <= i_V_reg_166;
            elsif (((ap_const_logic_1 = ap_sig_cseq_ST_st1_fsm_0) and not((ap_start = ap_const_logic_0)))) then 
                p_s_reg_103 <= ap_const_lv9_0;
            end if; 
        end if;
    end process;
    process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if (((ap_const_logic_1 = ap_sig_cseq_ST_st1_fsm_0) and not((ap_start = ap_const_logic_0)))) then
                data_nb_V_read_reg_153 <= data_nb_V;
                r_V_reg_158 <= r_V_fu_118_p2;
            end if;
        end if;
    end process;
    process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if ((ap_const_logic_1 = ap_sig_cseq_ST_st2_fsm_1)) then
                i_V_reg_166 <= i_V_fu_133_p2;
            end if;
        end if;
    end process;
    process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if (((ap_const_logic_1 = ap_sig_cseq_ST_st2_fsm_1) and not((tmp_2_fu_128_p2 = ap_const_lv1_0)))) then
                r_ostream_last_V_reg_176 <= r_ostream_last_V_fu_148_p2;
            end if;
        end if;
    end process;

    ap_NS_fsm_assign_proc : process (ap_start, ap_CS_fsm, tmp_2_fu_128_p2, ap_sig_ioackin_o_stream_TREADY)
    begin
        case ap_CS_fsm is
            when ap_ST_st1_fsm_0 => 
                if (not((ap_start = ap_const_logic_0))) then
                    ap_NS_fsm <= ap_ST_st2_fsm_1;
                else
                    ap_NS_fsm <= ap_ST_st1_fsm_0;
                end if;
            when ap_ST_st2_fsm_1 => 
                if ((tmp_2_fu_128_p2 = ap_const_lv1_0)) then
                    ap_NS_fsm <= ap_ST_st1_fsm_0;
                else
                    ap_NS_fsm <= ap_ST_st3_fsm_2;
                end if;
            when ap_ST_st3_fsm_2 => 
                if (not((ap_const_logic_0 = ap_sig_ioackin_o_stream_TREADY))) then
                    ap_NS_fsm <= ap_ST_st2_fsm_1;
                else
                    ap_NS_fsm <= ap_ST_st3_fsm_2;
                end if;
            when others =>  
                ap_NS_fsm <= "XXX";
        end case;
    end process;

    ap_done_assign_proc : process(ap_sig_cseq_ST_st2_fsm_1, tmp_2_fu_128_p2)
    begin
        if (((ap_const_logic_1 = ap_sig_cseq_ST_st2_fsm_1) and (tmp_2_fu_128_p2 = ap_const_lv1_0))) then 
            ap_done <= ap_const_logic_1;
        else 
            ap_done <= ap_const_logic_0;
        end if; 
    end process;


    ap_idle_assign_proc : process(ap_start, ap_sig_cseq_ST_st1_fsm_0)
    begin
        if (((ap_const_logic_0 = ap_start) and (ap_const_logic_1 = ap_sig_cseq_ST_st1_fsm_0))) then 
            ap_idle <= ap_const_logic_1;
        else 
            ap_idle <= ap_const_logic_0;
        end if; 
    end process;


    ap_ready_assign_proc : process(ap_sig_cseq_ST_st2_fsm_1, tmp_2_fu_128_p2)
    begin
        if (((ap_const_logic_1 = ap_sig_cseq_ST_st2_fsm_1) and (tmp_2_fu_128_p2 = ap_const_lv1_0))) then 
            ap_ready <= ap_const_logic_1;
        else 
            ap_ready <= ap_const_logic_0;
        end if; 
    end process;


    ap_rst_n_inv_assign_proc : process(ap_rst_n)
    begin
                ap_rst_n_inv <= not(ap_rst_n);
    end process;


    ap_sig_102_assign_proc : process(ap_CS_fsm)
    begin
                ap_sig_102 <= (ap_const_lv1_1 = ap_CS_fsm(1 downto 1));
    end process;


    ap_sig_20_assign_proc : process(ap_CS_fsm)
    begin
                ap_sig_20 <= (ap_CS_fsm(0 downto 0) = ap_const_lv1_1);
    end process;


    ap_sig_50_assign_proc : process(ap_CS_fsm)
    begin
                ap_sig_50 <= (ap_const_lv1_1 = ap_CS_fsm(2 downto 2));
    end process;


    ap_sig_cseq_ST_st1_fsm_0_assign_proc : process(ap_sig_20)
    begin
        if (ap_sig_20) then 
            ap_sig_cseq_ST_st1_fsm_0 <= ap_const_logic_1;
        else 
            ap_sig_cseq_ST_st1_fsm_0 <= ap_const_logic_0;
        end if; 
    end process;


    ap_sig_cseq_ST_st2_fsm_1_assign_proc : process(ap_sig_102)
    begin
        if (ap_sig_102) then 
            ap_sig_cseq_ST_st2_fsm_1 <= ap_const_logic_1;
        else 
            ap_sig_cseq_ST_st2_fsm_1 <= ap_const_logic_0;
        end if; 
    end process;


    ap_sig_cseq_ST_st3_fsm_2_assign_proc : process(ap_sig_50)
    begin
        if (ap_sig_50) then 
            ap_sig_cseq_ST_st3_fsm_2 <= ap_const_logic_1;
        else 
            ap_sig_cseq_ST_st3_fsm_2 <= ap_const_logic_0;
        end if; 
    end process;


    ap_sig_ioackin_o_stream_TREADY_assign_proc : process(o_stream_TREADY, ap_reg_ioackin_o_stream_TREADY)
    begin
        if ((ap_const_logic_0 = ap_reg_ioackin_o_stream_TREADY)) then 
            ap_sig_ioackin_o_stream_TREADY <= o_stream_TREADY;
        else 
            ap_sig_ioackin_o_stream_TREADY <= ap_const_logic_1;
        end if; 
    end process;

    i_V_fu_133_p2 <= std_logic_vector(unsigned(p_s_reg_103) + unsigned(ap_const_lv9_1));
        lhs_V_cast_fu_114_p1 <= std_logic_vector(resize(signed(data_nb_V),12));

    mem_V_address0 <= tmp_3_fu_139_p1(10 - 1 downto 0);

    mem_V_ce0_assign_proc : process(ap_sig_cseq_ST_st2_fsm_1)
    begin
        if ((ap_const_logic_1 = ap_sig_cseq_ST_st2_fsm_1)) then 
            mem_V_ce0 <= ap_const_logic_1;
        else 
            mem_V_ce0 <= ap_const_logic_0;
        end if; 
    end process;

    o_stream_TDATA <= mem_V_q0;

    o_stream_TDATA_blk_n_assign_proc : process(o_stream_TREADY, ap_sig_cseq_ST_st3_fsm_2)
    begin
        if ((ap_const_logic_1 = ap_sig_cseq_ST_st3_fsm_2)) then 
            o_stream_TDATA_blk_n <= o_stream_TREADY;
        else 
            o_stream_TDATA_blk_n <= ap_const_logic_1;
        end if; 
    end process;

    o_stream_TDEST <= ap_const_lv1_0;
    o_stream_TID <= ap_const_lv1_0;
    o_stream_TKEEP <= ap_const_lv8_7;
    o_stream_TLAST <= r_ostream_last_V_reg_176;
    o_stream_TSTRB <= ap_const_lv8_7;
    o_stream_TUSER <= ap_const_lv1_0;

    o_stream_TVALID_assign_proc : process(ap_sig_cseq_ST_st3_fsm_2, ap_reg_ioackin_o_stream_TREADY)
    begin
        if ((((ap_const_logic_1 = ap_sig_cseq_ST_st3_fsm_2) and (ap_const_logic_0 = ap_reg_ioackin_o_stream_TREADY)))) then 
            o_stream_TVALID <= ap_const_logic_1;
        else 
            o_stream_TVALID <= ap_const_logic_0;
        end if; 
    end process;

    r_V_fu_118_p2 <= std_logic_vector(signed(lhs_V_cast_fu_114_p1) + signed(ap_const_lv12_FFF));
    r_ostream_last_V_fu_148_p2 <= "1" when (tmp_6_cast_fu_144_p1 = r_V_reg_158) else "0";
    tmp_2_fu_128_p2 <= "1" when (signed(tmp_cast_fu_124_p1) < signed(data_nb_V_read_reg_153)) else "0";
        tmp_3_fu_139_p1 <= std_logic_vector(resize(signed(p_s_reg_103),64));

        tmp_6_cast_fu_144_p1 <= std_logic_vector(resize(signed(p_s_reg_103),12));

        tmp_cast_fu_124_p1 <= std_logic_vector(resize(signed(p_s_reg_103),11));

end behav;
