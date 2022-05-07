#!/usr/bin/perl

#  usage: files.perl < list

$suffix = "FV";
$mapfile = "/glade/work/nanr/mapfiles/map_ne120_to_0.23x0.31_bilinear.nc";

 while(<>)
 {
         @vars = split(/\s+/,$_);
         $ifile = @vars[0];
         $ofile = $ifile;
         $pt1 = substr($ofile,$ofile,(length($ofile)-2));
         $pt2 = substr($ofile,(length($ofile)-3),3);
         $newname = $pt1.$suffix.$pt2;
         #print("ncremap -m $mapfile -i $ifile.nc -o $newname; rm tmp.nc\n");
         print("ncremap -m $mapfile -i $ifile -o $newname\n");
 }

