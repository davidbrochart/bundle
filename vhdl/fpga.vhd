library ieee;
use ieee.std_logic_1164.all;
use work.bundlepack.all;

entity fpga is
    port (
    i_iter_data_nb  : in  array (0 to ITER_NB - 1) of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    i_iter_func_i   : in  array (0 to ITER_NB - 1) of std_logic_vector(FUNC_BITNB - 1 downto 0);
    i_iter_rmem0_i  : in  array (0 to ITER_NB - 1) of std_logic_vector(MEM_BITNB - 1 downto 0);
    i_iter_rmem1_i  : in  array (0 to ITER_NB - 1) of std_logic_vector(MEM_BITNB - 1 downto 0);
    i_iter_wmem_i   : in  array (0 to ITER_NB - 1) of std_logic_vector(MEM_BITNB - 1 downto 0);
    --u_ctrl[mem_i].array_ptr = array_ptr TODO
    ap_clk : IN STD_LOGIC;
    ap_rst_n : IN STD_LOGIC;
    ddr2fpga_stream_TDATA : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (63 downto 0);
    ddr2fpga_stream_TVALID : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    ddr2fpga_stream_TREADY : out array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    ddr2fpga_stream_TKEEP : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (7 downto 0);
    ddr2fpga_stream_TSTRB : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (7 downto 0);
    ddr2fpga_stream_TUSER : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (0 downto 0);
    ddr2fpga_stream_TLAST : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (0 downto 0);
    ddr2fpga_stream_TID : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (0 downto 0);
    ddr2fpga_stream_TDEST : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (0 downto 0);
    ddr2fpga_axi_ctrl_AWVALID : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    ddr2fpga_axi_ctrl_AWREADY : out array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    ddr2fpga_axi_ctrl_AWADDR : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_ADDR_WIDTH-1 downto 0);
    ddr2fpga_axi_ctrl_WVALID : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    ddr2fpga_axi_ctrl_WREADY : out array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    ddr2fpga_axi_ctrl_WDATA : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_DATA_WIDTH-1 downto 0);
    ddr2fpga_axi_ctrl_WSTRB : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_DATA_WIDTH/8-1 downto 0);
    ddr2fpga_axi_ctrl_ARVALID : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    ddr2fpga_axi_ctrl_ARREADY : out array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    ddr2fpga_axi_ctrl_ARADDR : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_ADDR_WIDTH-1 downto 0);
    ddr2fpga_axi_ctrl_RVALID : out array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    ddr2fpga_axi_ctrl_RREADY : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    ddr2fpga_axi_ctrl_RDATA : out array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_DATA_WIDTH-1 downto 0);
    ddr2fpga_axi_ctrl_RRESP : out array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (1 downto 0);
    ddr2fpga_axi_ctrl_BVALID : out array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    ddr2fpga_axi_ctrl_BREADY : in array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    ddr2fpga_axi_ctrl_BRESP : out array (0 to DDR2FPGA_NB - 1) of STD_LOGIC_VECTOR (1 downto 0);
    ddr2fpga_interrupt : out array (0 to DDR2FPGA_NB - 1) of STD_LOGIC;
    fpga2ddr_stream_TDATA : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (63 downto 0);
    fpga2ddr_stream_TVALID : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    fpga2ddr_stream_TREADY : in array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    fpga2ddr_stream_TKEEP : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (7 downto 0);
    fpga2ddr_stream_TSTRB : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (7 downto 0);
    fpga2ddr_stream_TUSER : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (0 downto 0);
    fpga2ddr_stream_TLAST : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (0 downto 0);
    fpga2ddr_stream_TID : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (0 downto 0);
    fpga2ddr_stream_TDEST : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (0 downto 0);
    fpga2ddr_axi_ctrl_AWVALID : in array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    fpga2ddr_axi_ctrl_AWREADY : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    fpga2ddr_axi_ctrl_AWADDR : in array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_ADDR_WIDTH-1 downto 0);
    fpga2ddr_axi_ctrl_WVALID : in array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    fpga2ddr_axi_ctrl_WREADY : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    fpga2ddr_axi_ctrl_WDATA : in array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_DATA_WIDTH-1 downto 0);
    fpga2ddr_axi_ctrl_WSTRB : in array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_DATA_WIDTH/8-1 downto 0);
    fpga2ddr_axi_ctrl_ARVALID : in array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    fpga2ddr_axi_ctrl_ARREADY : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    fpga2ddr_axi_ctrl_ARADDR : in array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_ADDR_WIDTH-1 downto 0);
    fpga2ddr_axi_ctrl_RVALID : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    fpga2ddr_axi_ctrl_RREADY : in array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    fpga2ddr_axi_ctrl_RDATA : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_DATA_WIDTH-1 downto 0);
    fpga2ddr_axi_ctrl_RRESP : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (1 downto 0);
    fpga2ddr_axi_ctrl_BVALID : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    fpga2ddr_axi_ctrl_BREADY : in array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    fpga2ddr_axi_ctrl_BRESP : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC_VECTOR (1 downto 0);
    fpga2ddr_interrupt : out array (0 to FPGA2DDR_NB - 1) of STD_LOGIC;
    iterator_axi_ctrl_AWVALID : in array (0 to ITERATOR_NB - 1) of STD_LOGIC;
    iterator_axi_ctrl_AWREADY : out array (0 to ITERATOR_NB - 1) of STD_LOGIC;
    iterator_axi_ctrl_AWADDR : in array (0 to ITERATOR_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_ADDR_WIDTH-1 downto 0);
    iterator_axi_ctrl_WVALID : in array (0 to ITERATOR_NB - 1) of STD_LOGIC;
    iterator_axi_ctrl_WREADY : out array (0 to ITERATOR_NB - 1) of STD_LOGIC;
    iterator_axi_ctrl_WDATA : in array (0 to ITERATOR_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_DATA_WIDTH-1 downto 0);
    iterator_axi_ctrl_WSTRB : in array (0 to ITERATOR_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_DATA_WIDTH/8-1 downto 0);
    iterator_axi_ctrl_ARVALID : in array (0 to ITERATOR_NB - 1) of STD_LOGIC;
    iterator_axi_ctrl_ARREADY : out array (0 to ITERATOR_NB - 1) of STD_LOGIC;
    iterator_axi_ctrl_ARADDR : in array (0 to ITERATOR_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_ADDR_WIDTH-1 downto 0);
    iterator_axi_ctrl_RVALID : out array (0 to ITERATOR_NB - 1) of STD_LOGIC;
    iterator_axi_ctrl_RREADY : in array (0 to ITERATOR_NB - 1) of STD_LOGIC;
    iterator_axi_ctrl_RDATA : out array (0 to ITERATOR_NB - 1) of STD_LOGIC_VECTOR (C_S_AXI_CTRL_DATA_WIDTH-1 downto 0);
    iterator_axi_ctrl_RRESP : out array (0 to ITERATOR_NB - 1) of STD_LOGIC_VECTOR (1 downto 0);
    iterator_axi_ctrl_BVALID : out array (0 to ITERATOR_NB - 1) of STD_LOGIC;
    iterator_axi_ctrl_BREADY : in array (0 to ITERATOR_NB - 1) of STD_LOGIC;
    iterator_axi_ctrl_BRESP : out array (0 to ITERATOR_NB - 1) of STD_LOGIC_VECTOR (1 downto 0);
    iterator_interrupt : out array (0 to ITERATOR_NB - 1) of STD_LOGIC
);
end fpga;

architecture rtl of fpga is
    signal s_mem_wena:          array (0 to MEM_NB - 1)         of std_logic;
    signal s_mem_addr:          array (0 to MEM_NB - 1)         of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    signal s_mem_din:           array (0 to MEM_NB - 1)         of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal s_mem_dout:          array (0 to MEM_NB - 1)         of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal s_iter_raddr:        array (0 to ITER_NB - 1)        of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    signal s_iter_waddr:        array (0 to ITER_NB - 1)        of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    signal s_iter_wena:         array (0 to ITER_NB - 1)        of std_logic;
    signal s_iter_arg_valid:    array (0 to ITER_NB - 1)        of std_logic;
    signal s_iter_res_valid:    array (0 to ITER_NB - 1)        of std_logic;
    signal s_iter_rmem0_i:      array (0 to ITER_NB - 1)        of std_logic_vector(MEM_BITNB - 1 downto 0);
    signal s_iter_rmem1_i:      array (0 to ITER_NB - 1)        of std_logic_vector(MEM_BITNB - 1 downto 0);
    signal s_iter_wmem_i:       array (0 to ITER_NB - 1)        of std_logic_vector(MEM_BITNB - 1 downto 0);
    signal s_iter_func_i:       array (0 to ITER_NB - 1)        of std_logic_vector(FUNC_BITNB - 1 downto 0);
    signal s_func_arg0:         array (0 to FUNC_NB - 1)        of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal s_func_arg1:         array (0 to FUNC_NB - 1)        of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal s_func_arg_valid:    array (0 to FUNC_NB - 1)        of std_logic;
    signal s_func_res:          array (0 to FUNC_NB - 1)        of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal s_func_res_valid:    array (0 to FUNC_NB - 1)        of std_logic;
    signal s_ddr2fpga_mem_i:    array (0 to DDR2FPGA_NB - 1)    of std_logic_vector(MEM_BITNB - 1 downto 0);
    signal s_ddr2fpga_data_nb:  array (0 to DDR2FPGA_NB - 1)    of std_logic_vector(MEM_DEPTH_BITNB downto 0);
    signal s_ddr2fpga_done:     array (0 to DDR2FPGA_NB - 1)    of std_logic;
    signal s_ddr2fpga_ack:      array (0 to DDR2FPGA_NB - 1)    of std_logic;
    signal s_fpga2ddr_mem_i:    array (0 to FPGA2DDR_NB - 1)    of std_logic_vector(MEM_BITNB - 1 downto 0);
    signal s_fpga2ddr_data_nb:  array (0 to FPGA2DDR_NB - 1)    of std_logic_vector(MEM_DEPTH_BITNB downto 0);
    signal s_fpga2ddr_done:     array (0 to FPGA2DDR_NB - 1)    of std_logic;
    signal s_fpga2ddr_ack:      array (0 to FPGA2DDR_NB - 1)    of std_logic;
    signal s_fpga2ddr_mem_dout: array (0 to FPGA2DDR_NB - 1)    of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal s_fpga2ddr_addr:     array (0 to FPGA2DDR_NB - 1)    of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    signal s_fpga2ddr_wena:     array (0 to FPGA2DDR_NB - 1)    of std_logic;
    signal s_ddr2fpga_wena:     array (0 to DDR2FPGA_NB - 1)    of std_logic;
    signal s_ddr2fpga_addr:     array (0 to DDR2FPGA_NB - 1)    of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    signal s_ddr2fpga_mem_din:  array (0 to DDR2FPGA_NB - 1)    of std_logic_vector(MEM_WIDTH - 1 downto 0);
begin
    GEN_DDR2FPGA_NB: for I in 0 to DDR2FPGA_NB - 1 generate
        u_ddr2fpga: ddr2fpga
        port map(
            ap_clk              => ap_clk,
            ap_rst_n            => ap_rst_n,
            i_stream_TDATA      => ddr2fpga_stream_TDATA    (I),
            i_stream_TVALID     => ddr2fpga_stream_TVALID   (I),
            i_stream_TREADY     => ddr2fpga_stream_TREADY   (I),
            i_stream_TKEEP      => ddr2fpga_stream_TKEEP    (I),
            i_stream_TSTRB      => ddr2fpga_stream_TSTRB    (I),
            i_stream_TUSER      => ddr2fpga_stream_TUSER    (I),
            i_stream_TLAST      => ddr2fpga_stream_TLAST    (I),
            i_stream_TID        => ddr2fpga_stream_TID      (I),
            i_stream_TDEST      => ddr2fpga_stream_TDEST    (I),
            mem_V_address0      => s_ddr2fpga_addr          (I),
            --mem_V_ce0
            mem_V_we0           => s_ddr2fpga_wena          (I),
            mem_V_d0            => s_ddr2fpga_din           (I),
            s_axi_ctrl_AWVALID  => ddr2fpga_axi_ctrl_AWVALID(I),
            s_axi_ctrl_AWREADY  => ddr2fpga_axi_ctrl_AWREADY(I),
            s_axi_ctrl_AWADDR   => ddr2fpga_axi_ctrl_AWADDR (I),
            s_axi_ctrl_WVALID   => ddr2fpga_axi_ctrl_WVALID (I),
            s_axi_ctrl_WREADY   => ddr2fpga_axi_ctrl_WREADY (I),
            s_axi_ctrl_WDATA    => ddr2fpga_axi_ctrl_WDATA  (I),
            s_axi_ctrl_WSTRB    => ddr2fpga_axi_ctrl_WSTRB  (I),
            s_axi_ctrl_ARVALID  => ddr2fpga_axi_ctrl_ARVALID(I),
            s_axi_ctrl_ARREADY  => ddr2fpga_axi_ctrl_ARREADY(I),
            s_axi_ctrl_ARADDR   => ddr2fpga_axi_ctrl_ARADDR (I),
            s_axi_ctrl_RVALID   => ddr2fpga_axi_ctrl_RVALID (I),
            s_axi_ctrl_RREADY   => ddr2fpga_axi_ctrl_RREADY (I),
            s_axi_ctrl_RDATA    => ddr2fpga_axi_ctrl_RDATA  (I),
            s_axi_ctrl_RRESP    => ddr2fpga_axi_ctrl_RRESP  (I),
            s_axi_ctrl_BVALID   => ddr2fpga_axi_ctrl_BVALID (I),
            s_axi_ctrl_BREADY   => ddr2fpga_axi_ctrl_BREADY (I),
            s_axi_ctrl_BRESP    => ddr2fpga_axi_ctrl_BRESP  (I),
            interrupt           => ddr2fpga_interrupt       (I)
        );
    end generate GEN_DDR2FPGA_NB;
    GEN_FPGA2DDR_NB: for I in 0 to FPGA2DDR_NB - 1 generate
        u_fpga2ddr: fpga2ddr
        port map(
            ap_clk              => ap_clk,
            ap_rst_n            => ap_rst_n,
            o_stream_TDATA      => fpga2ddr_stream_TDATA    (I),
            o_stream_TVALID     => fpga2ddr_stream_TVALID   (I),
            o_stream_TREADY     => fpga2ddr_stream_TREADY   (I),
            o_stream_TKEEP      => fpga2ddr_stream_TKEEP    (I),
            o_stream_TSTRB      => fpga2ddr_stream_TSTRB    (I),
            o_stream_TUSER      => fpga2ddr_stream_TUSER    (I),
            o_stream_TLAST      => fpga2ddr_stream_TLAST    (I),
            o_stream_TID        => fpga2ddr_stream_TID      (I),
            o_stream_TDEST      => fpga2ddr_stream_TDEST    (I),
            mem_V_address0      => s_fpga2ddr_addr          (I),
            --mem_V_ce0
            mem_V_q0            => s_fpga2ddr_dout          (I),
            s_axi_ctrl_AWVALID  => fpga2ddr_axi_ctrl_AWVALID(I),
            s_axi_ctrl_AWREADY  => fpga2ddr_axi_ctrl_AWREADY(I),
            s_axi_ctrl_AWADDR   => fpga2ddr_axi_ctrl_AWADDR (I),
            s_axi_ctrl_WVALID   => fpga2ddr_axi_ctrl_WVALID (I),
            s_axi_ctrl_WREADY   => fpga2ddr_axi_ctrl_WREADY (I),
            s_axi_ctrl_WDATA    => fpga2ddr_axi_ctrl_WDATA  (I),
            s_axi_ctrl_WSTRB    => fpga2ddr_axi_ctrl_WSTRB  (I),
            s_axi_ctrl_ARVALID  => fpga2ddr_axi_ctrl_ARVALID(I),
            s_axi_ctrl_ARREADY  => fpga2ddr_axi_ctrl_ARREADY(I),
            s_axi_ctrl_ARADDR   => fpga2ddr_axi_ctrl_ARADDR (I),
            s_axi_ctrl_RVALID   => fpga2ddr_axi_ctrl_RVALID (I),
            s_axi_ctrl_RREADY   => fpga2ddr_axi_ctrl_RREADY (I),
            s_axi_ctrl_RDATA    => fpga2ddr_axi_ctrl_RDATA  (I),
            s_axi_ctrl_RRESP    => fpga2ddr_axi_ctrl_RRESP  (I),
            s_axi_ctrl_BVALID   => fpga2ddr_axi_ctrl_BVALID (I),
            s_axi_ctrl_BREADY   => fpga2ddr_axi_ctrl_BREADY (I),
            s_axi_ctrl_BRESP    => fpga2ddr_axi_ctrl_BRESP  (I),
            interrupt           => fpga2ddr_interrupt       (I)
        );
    end generate GEN_FPGA2DDR_NB;
    GEN_MEM_NB: for I in 0 to MEM_NB - 1 generate
        u_mem: memory
        port map (
            i_addr  => s_mem_addr(I),
            i_wena  => s_mem_wena(I),
            i_din   => s_mem_din(I),
            o_dout  => s_mem_dout(I)
        );
    end generate GEN_MEM_NB;
    GEN_ITER_NB: for I in 0 to ITER_NB - 1 generate
        u_iter: iterator
        port map (
            o_raddr     => s_iter_raddr(I),
            o_waddr     => s_iter_waddr(I),
            o_wena      => s_iter_wena(I),
            o_arg_valid => s_iter_arg_valid(I),
            i_res_valid => s_iter_res_valid(I)
            s_axi_ctrl_AWVALID => iterator_axi_ctrl_AWVALID(I),
            s_axi_ctrl_AWREADY => iterator_axi_ctrl_AWREADY(I),
            s_axi_ctrl_AWADDR  => iterator_axi_ctrl_AWADDR (I),
            s_axi_ctrl_WVALID  => iterator_axi_ctrl_WVALID (I),
            s_axi_ctrl_WREADY  => iterator_axi_ctrl_WREADY (I),
            s_axi_ctrl_WDATA   => iterator_axi_ctrl_WDATA  (I),
            s_axi_ctrl_WSTRB   => iterator_axi_ctrl_WSTRB  (I),
            s_axi_ctrl_ARVALID => iterator_axi_ctrl_ARVALID(I),
            s_axi_ctrl_ARREADY => iterator_axi_ctrl_ARREADY(I),
            s_axi_ctrl_ARADDR  => iterator_axi_ctrl_ARADDR (I),
            s_axi_ctrl_RVALID  => iterator_axi_ctrl_RVALID (I),
            s_axi_ctrl_RREADY  => iterator_axi_ctrl_RREADY (I),
            s_axi_ctrl_RDATA   => iterator_axi_ctrl_RDATA  (I),
            s_axi_ctrl_RRESP   => iterator_axi_ctrl_RRESP  (I),
            s_axi_ctrl_BVALID  => iterator_axi_ctrl_BVALID (I),
            s_axi_ctrl_BREADY  => iterator_axi_ctrl_BREADY (I),
            s_axi_ctrl_BRESP   => iterator_axi_ctrl_BRESP  (I),
            interrupt          => iterator_interrupt       (I)
            
        );
    end generate GEN_ITER_NB;
    GEN_FUNC_NB: for I in 0 to FUNC_NB - 1 generate
        GEN_ADD_NB: if I < ADD_NB generate
            u_add: add
            port map (
                i_arg0      => s_func_arg0(I),
                i_arg1      => s_func_arg1(I),
                i_arg_valid => s_func_arg_valid(I),
                o_res       => s_func_res(I),
                o_res_valid => s_func_res_valid(I)
            );
        end generate GEN_ADD_NB;
        GEN_MUL_NB: if I >= ADD_NB and I < ADD_NB + MUL_NB generate
            u_mul: mul
            port map (
                i_arg0      => s_func_arg0(I),
                i_arg1      => s_func_arg1(I),
                i_arg_valid => s_func_arg_valid(I),
                o_res       => s_func_res(I),
                o_res_valid => s_func_res_valid(I)
            );
        end generate GEN_MUL_NB;
    end generate GEN_FUNC_NB;
    process(s_mem_addr, s_mem_din, s_mem_dout, s_mem_wena, s_fpga2ddr_mem_i, s_fpga2ddr_addr, s_ddr2fpga_mem_i, s_ddr2fpga_wena, s_ddr2fpga_addr, s_ddr2fpga_din, s_func_arg_valid, s_func_arg0, s_func_arg1, s_func_res_valid, s_iter_raddr, s_iter_waddr, s_iter_wena, s_iter_rmem0_i, s_iter_rmem1_i, s_iter_wmem_i, s_func_res, s_iter_func_i, s_iter_arg_valid)
    begin
        for I in 0 to MEM_NB - 1 loop
            s_mem_addr(I)   <= (others => '0');
            s_mem_din(I)    <= (others => '0');
            s_mem_wena(I)   <= (others => '0');
        end loop;
        for I in 0 to FPGA2DDR_NB - 1 loop
            s_mem_addr(s_fpga2ddr_mem_i(I)) <= s_mem_addr(s_fpga2ddr_mem_i(I)) or s_fpga2ddr_addr(I);
            s_fpga2ddr_mem_dout(I) <= s_mem_dout(s_fpga2ddr_mem_i(I));
        end loop;
        for I in 0 to DDR2FPGA_NB - 1 loop
            s_mem_wena(s_ddr2fpga_mem_i(I)) <= s_mem_wena(s_ddr2fpga_mem_i(I)) or s_ddr2fpga_wena(I);
            s_mem_addr(s_ddr2fpga_mem_i(I)) <= s_mem_addr(s_ddr2fpga_mem_i(I)) or s_ddr2fpga_addr(I);
            s_mem_din(s_ddr2fpga_mem_i(I))  <= s_mem_din(s_ddr2fpga_mem_i(I))  or s_ddr2fpga_din(I);
        end loop;
        for I in 0 to FUNC_NB - 1 loop
            s_func_arg_valid(I) <= (others => '0');
            s_func_arg0(I)      <= (others => '0');
            s_func_arg1(I)      <= (others => '0');
        end loop;
        for I in 0 to ITER_NB - 1 loop
            s_mem_addr(s_iter_rmem0_i(I))       <= s_mem_addr(s_iter_rmem0_i(I))      or s_iter_raddr(I);
            s_mem_addr(s_iter_rmem1_i(I))       <= s_mem_addr(s_iter_rmem1_i(I))      or s_iter_raddr(I);
            s_mem_addr(s_iter_wmem_i(I))        <= s_mem_addr(s_iter_wmem_i(I))       or s_iter_waddr(I);
            s_mem_wena(s_iter_wmem_i(I))        <= s_mem_wena(s_iter_wmem_i(I))       or s_iter_wena(I);
            s_mem_din(s_iter_wmem_i(I))         <= s_mem_din(s_iter_wmem_i(I))        or s_func_res(s_iter_func_i(I));
            s_func_arg_valid(s_iter_func_i(I))  <= s_func_arg_valid(s_iter_func_i(I)) or s_iter_arg_valid(I);
            if s_iter_arg_valid(I) = '1' then
                s_func_arg0(s_iter_func_i(I))   <= s_func_arg0(s_iter_func_i(I)) or s_mem_dout(s_iter_rmem0_i(I));
                s_func_arg1(s_iter_func_i(I))   <= s_func_arg1(s_iter_func_i(I)) or s_mem_dout(s_iter_rmem1_i(I));
            end if;
            s_iter_res_valid(I) <= s_func_res_valid(s_iter_func_i(I));
        end loop;
    end process;
end;
