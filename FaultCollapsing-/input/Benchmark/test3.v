module sample (N1,N2,N4); 
input N1,N2;
output N6;
wire N5;
//Gates in the module
OR2X1 AND_1 (.Y(N5),.A(N1),.B(N2)); 
INVX1 INV_1 (.Y(N4),.A(N5));
BUFX1 BUFF1_109 (.Y(N6),.A(N4));
endmodule
