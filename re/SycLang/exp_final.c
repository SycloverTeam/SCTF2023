int read(char* flag){}
int writes(){}
int writef(){}
int exit(){}

struct exp
{
    int key[24];
    int L[8];
    int R[8];
    int X[8];
};

int main(){
    char flag[24]; // sctf{r5cbsumyqpjy0stc7u}
    int key1;      // sctf{tHis_1s_fAkE_fLag!}
    int key2;
    int key3;
    int i;
    int x,kx;
    int y,ky;
    int z,kz;

    struct exp e1;
    struct exp e2;
    struct exp e3;
    struct exp e4;
    
    read(flag);

    for(i=0;i<24;i++){
        key1 = 0;
        x = i;
        key1 = flag[x];
        y = 23 - i;
        e1.key[y] = key1;
    }

    for(i=23;i>0;i--){
        y = i;
        ky = e1.key[y];
        x = i - 1;
        kx = e1.key[x]; 
        kz = ky - kx;
        e1.key[i] = kz; 
    }

    e1.L[0] = 0;
    e1.R[0] = 8;
    e1.X[0] = 11;
    e1.L[1] = 15;
    e1.R[1] = 23;
    e1.X[1] = 0-13;
    e1.L[2] = 2;
    e1.R[2] = 11;
    e1.X[2] = 17;
    e1.L[3] = 10;
    e1.R[3] = 20;
    e1.X[3] = 0-19;
    e1.L[4] = 6;
    e1.R[4] = 13;
    e1.X[4] = 23;
    e1.L[5] = 9;
    e1.R[5] = 21;
    e1.X[5] = 0-29;
    e1.L[6] = 1;
    e1.R[6] = 19;
    e1.X[6] = 31;
    e1.L[7] = 4;
    e1.R[7] = 17;
    e1.X[7] = 0-37;

    for(i=0;i<8;i++){
        x = e1.L[i];
        y = e1.R[i];
        z = e1.X[i];
        kx = e1.key[x];
        ky = e1.key[y];
        kx += z;
        ky -= z; 
        e1.key[x] = kx;
        e1.key[y] = ky;
    }

    for(i=1;i<24;i++){
        kx = e1.key[i];
        x = i-1;
        z = e1.key[x];
        kx += z;
        e1.key[i] = kx;
    }

    // xor
    for(i=0;i<23;i++){
        x = i;
        key1 = e1.key[x];
        y = i + 1;
        key2 = e1.key[y];
        key2 = 0;
        key3 = key1 ^ key2;
        e1.key[x] = key3;
    }

    // mix
    e3.L[0] = 0;
    e3.R[0] = 12;
    e3.X[0] = 0-19;
    e3.L[1] = 9;
    e3.R[1] = 10;
    e3.X[1] = 0-10;
    e3.L[2] = 9;
    e3.R[2] = 12;
    e3.X[2] = 3;
    e3.L[3] = 8;
    e3.R[3] = 19;
    e3.X[3] = 0-11;
    e3.L[4] = 10;
    e3.R[4] = 12;
    e3.X[4] = 0-9;
    e3.L[5] = 9;
    e3.R[5] = 13;
    e3.X[5] = 3;
    e3.L[6] = 1;
    e3.R[6] = 22;
    e3.X[6] = 0-19;
    e3.L[7] = 0;
    e3.R[7] = 23;
    e3.X[7] = 7;

    e3.key[0]=12;
    e3.key[1]=31;
    e3.key[2]=31;
    e3.key[3]=31;
    e3.key[4]=31;
    e3.key[5]=31;

    e3.key[6]=31;
    e3.key[7]=31;
    e3.key[8]=42;
    e3.key[9]=46;
    e3.key[10]=45;
    e3.key[11]=45;

    e3.key[12]=20;
    e3.key[13]=23;
    e3.key[14]=23;
    e3.key[15]=23;
    e3.key[16]=23;
    e3.key[17]=23;

    e3.key[18]=23;
    e3.key[19]=12;
    e3.key[20]=12;
    e3.key[21]=12;
    e3.key[22]=0-7;
    e3.key[23]=0; 

    for(i=23;i>0;i--){
        y = i;
        ky = e3.key[y];
        x = i - 1;
        kx = e3.key[x]; 
        kz = ky - kx;
        e3.key[i] = kz; 
    }

    for(i=0;i<8;i++){
        x = e3.L[i];
        y = e3.R[i];
        z = e3.X[i];
        kx = e3.key[x];
        ky = e3.key[y];
        kx += z;
        ky -= z; 
        e3.key[x] = kx;
        e3.key[y] = ky;
    }

    for(i=1;i<24;i++){
        kx = e3.key[i];
        x = i-1;
        z = e3.key[x];
        kx += z;
        e3.key[i] = kx;
    }

    e2.key[0]=252;
    e2.key[1]=352;
    e2.key[2]=484;
    e2.key[3]=470;
    e2.key[4]=496;
    e2.key[5]=487;

    e2.key[6]=539;
    e2.key[7]=585;
    e2.key[8]=447;
    e2.key[9]=474;
    e2.key[10]=577;
    e2.key[11]=454;

    e2.key[12]=466;
    e2.key[13]=345;
    e2.key[14]=344;
    e2.key[15]=486;
    e2.key[16]=501;
    e2.key[17]=423;

    e2.key[18]=490;
    e2.key[19]=375;
    e2.key[20]=257;
    e2.key[21]=203;
    e2.key[22]=265;
    e2.key[23]=125; 

    // xor2
    for(i=0;i<24;i++){
        x = i;
        kx = e2.key[x];
        y = i;
        ky = e3.key[y];
        kz = kx ^ ky;
        e2.key[i] = kz;
    }
    
    // twice
    for(i=0;i<8;i++){
        x = i + i + i;
        kx = e1.key[x];
        e2.X[i] = kx;
    }

    for(i=23;i>0;i--){
        y = i;
        ky = e2.key[y];
        x = i;
        x -= 1;
        kx = e2.key[x];
        kz = ky - kx;
        e2.key[i] = kz; 
    }

    for(i=0;i<8;i++){
        x = e1.L[i];
        y = e1.R[i];
        z = e2.X[i];
        kx = e2.key[x];
        ky = e2.key[y];
        kx -= z;
        ky += z; 
        e2.key[x] = kx;
        e2.key[y] = ky;
    }

    for(i=1;i<24;i++){
        kx = e2.key[i];
        x = i-1;
        z = e2.key[x];
        kx += z;
        e2.key[i] = kx;
    }

    // mix2
    for(i=0;i<7;i++){
        x = i;
        kx = e1.L[x];
        y = i + 1;
        ky = e1.L[y];
        kz = kx ^ ky;
        if(kz > 23){
            kz = 23;
        }
        e4.L[i] = kz;
    }
    e4.L[7] = 0;

    for(i=0;i<7;i++){
        x = i;
        kx = e1.R[x];
        y = i + 1;
        ky = e1.R[y];
        kz = kx ^ ky;
        if(kz > 23){
            kz = 23;
        }
        e4.R[i] = kz;
    }
    e4.R[7] = 23;  

    for(i=0;i<7;i++){
        x = i;
        kx = e1.X[x];
        y = i + 1;
        ky = e1.X[y];
        kz = kx ^ ky;
        e4.X[i] = kz;
    }
    e4.X[7] = 12;  

    e4.key[0] = 127;
    e4.key[1] = 111;
    e4.key[2] = 188;
    e4.key[3] = 174;
    e4.key[4] = 195;
    e4.key[5] = 128;
    e4.key[6] = 88;
    e4.key[7] = 121;
    e4.key[8] = 123;
    e4.key[9] = 103;
    e4.key[10] = 57;
    e4.key[11] = 123;
    e4.key[12] = 97;
    e4.key[13] = 74;
    e4.key[14] = 37;
    e4.key[15] = 59;
    e4.key[16] = 21;
    e4.key[17] = 47;
    e4.key[18] = 54;
    e4.key[19] = 28;
    e4.key[20] = 49;
    e4.key[21] = 55;
    e4.key[22] = -15;
    e4.key[23] = 125;

    for(i=23;i>0;i--){
        y = i;
        ky = e4.key[y];
        x = i;
        x -= 1;
        kx = e4.key[x];
        kz = ky - kx;
        e4.key[i] = kz; 
    }

    for(i=0;i<8;i++){
        x = e4.L[i];
        y = e4.R[i];
        z = e4.X[i];
        kx = e4.key[x];
        ky = e4.key[y];
        kx -= z;
        ky += z; 
        e4.key[x] = kx;
        e4.key[y] = ky;
    }

    for(i=1;i<24;i++){
        kx = e4.key[i];
        x = i-1;
        z = e4.key[x];
        kx += z;
        e4.key[i] = kx;
    }

    key1 = 0;
    key2 = 0;
    for(i=0; i<24; i){
        x = i;
        key1 = e1.key[i];
        y = i;
        key2 = e2.key[y];
        if(key2 != key1){
            writef();
            exit();
        }
        i = i+1;
    }
    writes();
    exit();
}

