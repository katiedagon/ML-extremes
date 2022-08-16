;************************************************
;
; These files are loaded by default in NCL V6.2.0 and newer
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;************************************************
function uvlev_func(dates)
begin
  ;tmpdir        = getenv("TMPDIR")
  ;filebeg       = getenv("FILEBEG")
  ;dates          = getenv("DATES")
  ;wind          = getenv("WIND")
  ;i1            = getenv("I1")
;************************************************
; file handling
;************************************************
  tmpdir = "/glade/scratch/kdagon/FrontDetector/B20TRC5CN"
  filebeg = "b.e13.B20TRC5CN.ne120_g16.003.cam.h0"
  wind = "U" ; zonal wind
  ;dates = "208601-208612"  

  ufilename=tmpdir+"/"+filebeg+"."+wind+"."+dates+".nc"
  pfilename=tmpdir+"/"+filebeg+".PS."+dates+".nc"
  in = addfile(ufilename, "r")
  inp = addfile(pfilename, "r")
;************************************************
; read needed variables from file
;************************************************
   u = in->$wind$                                    ; select variable to ave

   P0mb =1000.
   hyam = in->hyam                             ; get a coefficiants
   hybm = in->hybm                             ; get b coefficiants
   PS   = inp->PS                              ; get pressure
   printVarSummary(PS)
;************************************************
; define other arguments required by vinth2p
;************************************************
; type of interpolation: 1 = linear, 2 = log, 3 = loglog
   interp = 2 

; is extrapolation desired if data is outside the range of PS
   extrap = False

; create an array of desired pressure levels:
   plevo = (/ 850.0,500.0,300.0,200.0 /)            
   plevoc = (/ "850","500","300","200" /)            
   plevo@units = "hPa"
   plevo!0     = "plevo"

;************************************************
; calculate T on pressure levels
;************************************************
; note, the 7th argument is not used, and so is set to 1.
;************************************************
   printVarSummary(u)
   UonP = vinth2p_nodes(u(:,:,:),hyam,hybm,plevo,PS(:,:),interp,P0mb,1,extrap)
   printVarSummary(UonP)
   do level=0,3
     fout=tmpdir+"/"+filebeg+"."+wind+plevoc(level)+"."+dates+".nc"
     ;system("rm -f "+fout)   ; remove any pre-existing file
     ncdf = addfile(fout ,"c")  ; open output netCDF file
  ;===================================================================
  ; create global attributes of the file (optional)
  ;===================================================================
     fAtt               = True            ; assign file attributes
     fAtt@data_title         = "Monthly averaged/Zonal Wind/"+plevoc(level)
     fAtt@data_summary       = "Create input for ClimateNet application"
     fAtt@data_creator       = "Katie Dagon, kdagon@ucar.edu"
     fAtt@cesm_contact       = "John Truesdale, jet@ucar.edu"
     fAtt@data_script        = "ncl script using vinth2p_nodes"
     fAtt@source_file        =  ufilename+" and "+pfilename
     fAtt@Conventions        = "CF 1.0"
     fAtt@creation_date = systemfunc ("date")
     fileattdef( ncdf, fAtt )            ; copy file attributes

  ;===================================================================
  ; make time an UNLIMITED dimension; recommended  for most applications
  ;===================================================================
     filedimdef(ncdf,"time",-1,True) 
     vname=wind+plevoc(level)
     print(vname)
     ulev=UonP(:,level,:)
     ulev@units = "m/s"
     ulev@long_name = "Zonal wind at "+plevoc(level)+" mbar pressure surface" ;
     ncdf->$vname$  = ulev
     delete(ulev)
   end do

return("done")

end
