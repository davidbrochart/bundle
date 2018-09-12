library ieee;
use ieee.std_logic_1164.all;
use work.bundlepack.all;

entity iterator is
    generic (
    C_S_AXI_CTRL_ADDR_WIDTH : INTEGER := 5;
    C_S_AXI_CTRL_DATA_WIDTH : INTEGER := 32 );

    port (
    i_res_valid : in  std_logic;
    o_raddr     : out std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    o_waddr     : out std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    o_wena      : out std_logic;
    o_arg_valid : out std_logic;
    -- copied from HLS
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
    ap_clk : IN STD_LOGIC;
    ap_rst_n : IN STD_LOGIC;
    interrupt : OUT STD_LOGIC
);
end iterator;

architecture rtl of iterator is
    type t_state is (IDLE, ITERATING, FINISHING, COMPLETE);
    signal r_state:     t_state;
    signal r_arg_valid: std_logic;
    signal r_raddr:     std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    signal r_waddr:     std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    signal r_done:      std_logic;
    -- copied from HLS
    attribute CORE_GENERATION_INFO : STRING;
    attribute CORE_GENERATION_INFO of behav : architecture is
    "iterator,hls_ip_2016_1,{HLS_INPUT_TYPE=cxx,HLS_INPUT_FLOAT=0,HLS_INPUT_FIXED=1,HLS_INPUT_PART=xc7z020clg400-1,HLS_INPUT_CLOCK=10.000000,HLS_INPUT_ARCH=others,HLS_SYN_CLOCK=0.000000,HLS_SYN_LAT=0,HLS_SYN_TPT=none,HLS_SYN_MEM=0,HLS_SYN_DSP=0,HLS_SYN_FF=53,HLS_SYN_LUT=62}";
    constant ap_const_logic_1 : STD_LOGIC := '1';
    constant C_S_AXI_DATA_WIDTH : INTEGER range 63 downto 0 := 20;
    constant ap_const_logic_0 : STD_LOGIC := '0';

    signal ap_start : STD_LOGIC;
    signal ap_done : STD_LOGIC;
    signal ap_idle : STD_LOGIC;
    signal ap_ready : STD_LOGIC;
    signal data_nb_V : STD_LOGIC_VECTOR (10 downto 0);
    signal ap_rst_n_inv : STD_LOGIC;

    component iterator_ctrl_s_axi IS
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
        data_nb_V : OUT STD_LOGIC_VECTOR (10 downto 0) );
    end component;
begin
    process (ap_clk, ap_rst_n)
    begin
        if ap_rst_n = '0' then
            r_state         <= IDLE;
            r_arg_valid     <= '0';
            r_raddr         <= (others => '0');
            r_waddr         <= (others => '0');
            r_done          <= '0';
        elsif ap_clk = '1' and ap_clk'event then
            case r_state is
                when IDLE =>
                    if data_nb_V /= (data_nb_V'range => '0') then
                        r_state     <= ITERATING;
                    end if;
                when ITERATING =>
                    r_arg_valid <= '1';
                    if r_raddr = std_logic_vector(conv_unsigned(conv_integer(unsigned(data_nb_V)) - 1, MEM_DEPTH_BITNB - 1)) then
                        r_state <= FINISHING;
                    end if;
                when FINISHING =>
                    r_arg_valid <= '0';
                    if (r_waddr = std_logic_vector(conv_unsigned(conv_integer(unsigned(data_nb_V)) - 1, MEM_DEPTH_BITNB - 1))) and (i_res_valid = '1') then
                        r_state <= COMPLETE;
                        r_done  <= '1';
                    end if;
                when COMPLETE =>
                    r_done      <= '0';
                    if data_nb_V = (data_nb_V'range => '0') then
                        r_state     <= IDLE;
                        r_raddr     <= (others => '0');
                        r_waddr     <= (others => '0');
                        r_arg_valid <= (others => '0');
                    end if;
                when others =>
                    r_state <= IDLE;
            end case;
            if r_state = ITERATING then
                if r_raddr /= std_logic_vector(conv_unsigned(conv_integer(unsigned(data_nb_V)) - 1, MEM_DEPTH_BITNB - 1)) then
                    r_raddr <= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_raddr)) + 1, MEM_DEPTH_BITNB - 1));
                end if;
            end if;
            if (r_state = ITERATING) or (r_state = FINISHING) then
                if i_res_valid = '1' then
                    if r_waddr /= std_logic_vector(conv_unsigned(conv_integer(unsigned(data_nb_V)) - 1, MEM_DEPTH_BITNB - 1)) then
                        r_waddr <= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_waddr)) + 1, MEM_DEPTH_BITNB - 1));
                    end if;
                end if;
            end if;
        end if;
    end process;

    o_raddr     <= r_raddr;
    o_waddr     <= r_waddr;
    o_wena      <= i_res_valid when (r_state = ITERATING) or (r_state = FINISHING) else
                   '0';
    o_arg_valid <= r_arg_valid;

    -- copied from HLS
    iterator_ctrl_s_axi_U : component iterator_ctrl_s_axi
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
        data_nb_V => data_nb_V);




    -- Following line commented out because task done when iterator done
    --ap_done <= ap_start;
    ap_done <= r_done;
    ap_idle <= ap_const_logic_1;
    ap_ready <= ap_start;

    ap_rst_n_inv_assign_proc : process(ap_rst_n)
    begin
                ap_rst_n_inv <= not(ap_rst_n);
    end process;
end;
