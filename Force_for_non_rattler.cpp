#include<iostream>
#include<iomanip>
#include<fstream>
#include<math.h>
using namespace std;

int N=20000;
long double *ATOMx = new long double [N];
long double *ATOMy = new long double [N];
long double *ATOMz = new long double [N];

long double *nrATOMx = new long double [N];
long double *nrATOMy = new long double [N];

long double *overlap= new long double [N];
long double *RAD= new long double [N];
int *rat = new int[N];

long double *Forces= new long double [N];
long double *Forcesx= new long double [N];
long double *Forcesy= new long double [N];

int main( int argc , char * argv[] )
{
	std::ifstream infile(argv[1]);
	std::ofstream outfile(argv[2]);
	std::ofstream outfileconf(argv[5]);
	long double gamma=atof(argv[3]);
	long double a,b,c,d,e;
	long double BOX=2*atof(argv[4]);
	//N=atoi(argv[5]);
	long double tilt=gamma*BOX*0.0001;
	int index=0;
	while(infile>>a>>b>>c>>d>>e)
	{
		//cout<<b<<"\t"<<c<<"\t"<<d<<"\t"<<e<<"\n";
		ATOMx[index]=c;
		ATOMy[index]=d;
		//RAD[index]=e;
		if ( int(b)==1 )
			RAD[index]=0.5;
		if ( int(b)==2 )
			RAD[index]=0.7;
		
		overlap[index]=0;
		rat[index]=0;
		index++;
	}

	long double delta_rx,delta_ry,delta_rz;
    long double delta_r;

	int overlapsold=0;
	while(1)
	{
		for(int i=0;i<N-1;i++)
		{
			for(int j=i+1; j<N;j++)
			{
				if( rat[i] == 0 and rat[j] == 0)
				{
					delta_rx=ATOMx[i]-ATOMx[j];
					delta_ry=ATOMy[i]-ATOMy[j];
					//delta_rz=ATOMz[i]-ATOMz[j];

					delta_rx=(delta_rx-(tilt*lroundl(delta_ry/BOX)));
					delta_rx=(delta_rx-(BOX*lroundl(delta_rx/BOX)));
					delta_ry=(delta_ry-(BOX*lroundl(delta_ry/BOX)));
					//delta_rz=(delta_rz-(BOX*lroundl(delta_rz/BOX)));

					delta_r=delta_rx*delta_rx+delta_ry*delta_ry;//+delta_rz*delta_rz;
					delta_r=sqrt(delta_r);

					if(delta_r< RAD[i]+RAD[j])
					{
						//outfile<<i<<"\t"<<j<<"\t"<<delta_r<<"\t"<<RAD[i]<<"\t"<<RAD[j]<<"\n";
						//outfile<<i<<"\t"<<j<<"\n";//<<delta_r<<"\t"<<RAD[i]<<"\t"<<RAD[j]<<"\n";
                        
						overlap[i]++;
						overlap[j]++;
					}
				}
			}
		}
		int overlaps_NR=0;
		int NR=0;
		int overlaps=0;
		int R=0;
		for(int i=0;i<N;i++)
		{
            //Forces[i]=Forcesx[i]*Forcesx[i]+Forcesy[i]*Forcesy[i];
            //cout<<i<<"\t"<<Forces[i]<<"\n";
			if(overlap[i]<3)
			{
				rat[i]=1;
				R++;
				
			}
			if(overlap[i]>2)
			{
                
				overlaps_NR=overlaps_NR+overlap[i];
				NR++;

			}
            else
            {
               ;// cout<<i<<"\t"<<overlap[i]<<"\n";
            }
			overlaps=overlaps+overlap[i];
			
			overlap[i]=0;
		}
        //return(0);
		//cout<<R<<"\n";
		if(overlaps == overlapsold)
		{
			
			int nr_count=0;
            //NR=N;
			long double *nrATOMx = new long double [NR];
			long double *nrATOMy = new long double [NR];
			long double *nrRAD = new long double [NR];
			for(int i=0;i<N;i++)
			{
                Forcesx[i]=0.;
                Forcesy[i]=0.;
				if(rat[i]==0)
				{
					nrATOMx[nr_count]=ATOMx[i];
					nrATOMy[nr_count]=ATOMy[i];
					nrRAD[nr_count]=RAD[i];
                    
					nr_count=nr_count+1;
					outfileconf<<std::setprecision(16);
					if(RAD[i]==0.5)
						outfileconf<<nr_count<<"\t"<<"1\t"<<ATOMx[i]<<"\t"<<ATOMy[i]<<"\t0.5\n";
					if(RAD[i]==0.7)
						outfileconf<<nr_count<<"\t"<<"2\t"<<ATOMx[i]<<"\t"<<ATOMy[i]<<"\t0.7\n";
				}
                if(rat[i]!=0)
                {
                    //cout<<i<<"\t"<<nr_count<<"\n";
                }
			}
            //NR=N;
            //cout<<i<<"\t"<<nrRAD[0]<<"\n";
			//cout<<NR<<"\n";
			for(int i=0;i<NR-1;i++)
			{

                //cout<<i<<"\t"<<nrRAD[0]<<"\n";
				for(int j=i+1; j<NR;j++)
				{
					//if( rat[i] == 0 and rat[j] == 0)
					{
						delta_rx=nrATOMx[i]-nrATOMx[j];
						delta_ry=nrATOMy[i]-nrATOMy[j];
						//delta_rz=nrATOMz[i]-nrATOMz[j];

						delta_rx=(delta_rx-(tilt*lroundl(delta_ry/BOX)));
						delta_rx=(delta_rx-(BOX*lroundl(delta_rx/BOX)));
						delta_ry=(delta_ry-(BOX*lroundl(delta_ry/BOX)));
						//delta_rz=(delta_rz-(BOX*lroundl(delta_rz/BOX)));

						delta_r=delta_rx*delta_rx+delta_ry*delta_ry;//+delta_rz*delta_rz;
						delta_r=sqrt(delta_r);

						if(delta_r< nrRAD[i]+nrRAD[j])
						{
                            long double sigma =	nrRAD[i]+nrRAD[j];
                            long double F=(-2.*(1-delta_r/sigma)*(1./sigma));
                            Forcesx[i]=Forcesx[i]+F*delta_rx/delta_r;
                            Forcesy[i]=Forcesy[i]+F*delta_ry/delta_r;
                            Forcesx[j]=Forcesx[j]+-1.*F*delta_rx/delta_r;
                            Forcesy[j]=Forcesy[j]+-1.*F*delta_ry/delta_r;
                            outfile<<i<<"\t"<<j<<"\t"<<delta_r<<"\t"<<F*delta_rx/delta_r<<"\t"<<F*delta_ry/delta_r<<"\t"<<F<<"\n";//<<RAD[i]<<"\t"<<RAD[j]<<"\n";
							//cout<<i<<"\t"<<j<<"\t"<<delta_r<<"\t"<<nrRAD[i]<<"\t"<<nrRAD[j]<<"\n";
							//outfile<<i<<"\t"<<j<<"\n";//<<delta_r<<"\t"<<RAD[i]<<"\t"<<RAD[j]<<"\n";
							//overlap[i]++;
							//overlap[j]++;
						}
					}
				}
			}
            for(int i=0;i<NR;i++)
            {
                Forces[i]=Forcesx[i]*Forcesx[i]+Forcesy[i]*Forcesy[i];
                //cout<<i<<"\t"<<Forces[i]<<"\n";
            }
			if(NR)
				cout<<overlaps*1./(N)<<"\t"<<overlaps_NR*1./(NR)<<"\n";
			else 
				cout<<0.<<"\t"<<0.<<"\n";
			break;
		}
		else 
		{
			overlapsold=overlaps;
		}
	}
return 1;
}

