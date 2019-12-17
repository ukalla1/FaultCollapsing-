module sample(N1, N2, N4);

input N1,N2;
output N4;
wire N5;

ANDX1 AND_1 (.Y(N5),.A(N1),.B(N2));
INVX1 INV_1 (.Y(N4),.A(N5));

endmodule