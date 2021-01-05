#for f in init_18_D init_26_D init_14_D
#do 
	#cd $f 
		#cd 0.006/UNIFORM/
#ls -1v after_*.xyz > list 
#cp ../../../*.cpp . 
#cp ../../../*.py . 
#g++ 2d_pebble_game_frictionless.cpp
g++ Force_for_non_rattler.cpp
#g++ recursive_rat_rem.cpp
#BOX=26.2107109945647245
BOX=82.779329864587510
#cat list 
for i in $(cat list)
do
	n=`echo $i | awk -F '_' '{print $2}'`
	gamma=`echo "$n" | bc -l`
	tail -n 20000 $i > config_$gamma
	tilt=`echo "$gamma*2*$BOX*0.0001" | bc -l`
	#echo $tilt
	#python2.7 multiply_conf.py conf $BOX $tilt > newconf
	#tilt=`head -n 6 $i | tail -n 1 | awk '{print $3}'`
	#gamma=`echo "$tilt/(2*$BOX)" | bc -l`
	#echo $gamma
	#newBOX=`echo $BOX*3 | bc -l`
    ./a.out config_$gamma edges_$gamma $gamma $BOX conf_$gamma
    #./a.out config_$gamma edges_$gamma $gamma $BOX conf_$gamma
    Nnr=`wc conf_$gamma | awk '{print $1}'`
    python3 force_tile.py edges_$gamma $Nnr $gamma
    #cp FTN.pdf FTN_${gamma}.pdf
    cp network.dat network_${gamma}.dat 
    cp edges edges_${gamma}.dat 
    Nv=`wc vertices.dat | awk '{print $1}'` 
	mv vertices.dat vertices_${gamma}.dat
    echo $Nv
    #python PEBBLE_GAME/2d_pebble.py network_${gamma}.dat $Nv
    #mv network.pdf pebble_FTN_${gamma}.pdf
   	#echo $gamma $znr >> gamma_recursive.dat 
	#python2.7 logbin.py F_total.dat_$gamma > F_total_dis_$gamma
	#awk '{print 1,-1*$5}' edges_$gamma > forces_$gamma
	#python2.7 logbin.py forces_$gamma > f_dis_$gamma
	#NR=`wc nr_conf | awk '{print $1}'`
    #python2.7 2d_pebble.py edges $gamma $BOX $NR
    #echo $gamma $out >> gamma_z_nr.dat
done
		#cd ../../
	#cd ../
#done 
