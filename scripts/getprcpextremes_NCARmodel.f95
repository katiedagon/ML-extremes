program getprcpextremes

!*******************************************************************************
! This program identifies the top N precipitaion events from gridded data
! where N = Nyear/RETURN, Nyear=number of years in time series, RETURN =
! recurrence interval
! The configuration is for a 1 degree longitude by 1 degree latitude resolution
! grid, data availabiliy up to 221 years (1800-2019)
! The program outputs the year, day, precip amount for each event and the number
! of events in each year
! Input parameters are RETURN, the duration (DURATION) of events,
! the beginning year (BegYear), and end year (EndYear)
!*******************************************************************************
! Variable Declarations

integer, parameter :: MAXLONG=360
integer, parameter :: MAXLAT=180
integer, parameter :: BYR=1800
integer, parameter :: EYR=2019
integer, parameter :: MISS=-99
integer :: RETURN,DURATION,BegYear,EndYear
integer, dimension(1:81000) :: lYr,lDy
integer, dimension(1:221) :: event
integer, parameter :: rMiss=-99
integer, allocatable, dimension(:) :: yearcount
real, allocatable, dimension(:,:,:,:) :: rData
real, dimension(1:81000) :: rGrid
real, dimension(1:221) :: amount
real :: psum
character(len=40) :: aa

allocate(rData(1:MAXLONG,1:MAXLAT,BYR:EYR,1:366))
allocate(yearcount(BYR:EYR))

event(:)=0
yearcount(:)=0
amount(:)=0
rData(:,:,:,:)=rMiss
rGrid(:)=rMiss
lYr(:)=MISS
lDy(:)=MISS

call getarg(1,aa)
read(aa,'(i6)')RETURN
call getarg(2,aa)
read(aa,'(i6)')DURATION
call getarg(3,aa)
read(aa,'(i6)')BegYear
call getarg(4,aa)
read(aa,'(i6)')EndYear


!*******************************************************************************
! INSERT CODE HERE To Read in Model Data into array rData

!*******************************************************************************
! Master Processing Loop (loop through each gridpoint)

do iLong = 1,MAXLONG

do iLat = 1,MAXLAT

!*******************************************************************************
! Convert 2-dimensional array (year, day) into 1-dimensional array
! with jday=1 for year=BegYear and day=1
!*******************************************************************************

jday=0
do iY=BegYear,EndYear
   jEND=365
   if(4*int((iY)/4).eq.iY)jEND=366

   do iD=1,jEND
   jday=jday+1
   rGrid(jday) = rData(iLong,iLat,iY,iD)
   lYr(jday)=iY
   lDy(jday)=iD
   enddo

   enddo

nevents=0

!*******************************************************************************
! IDENTIFY HEAVY PRECIP EVENTS
!*******************************************************************************

iNEV=nint(1.*(EndYear-BegYear+1)/RETURN)
rMax=0
num=0
 do ie=1,iNEV
 rMax=0
 do iD=1,jday
      psum=0
      do jD=iD,iD+DURATION-1
        if(rGrid(jD).eq.rMiss)goto 35
        psum=psum+rGrid(jD)
      enddo
      if(rMax.le.psum)then
        rMax=psum
        kD=iD
        endif
    35 enddo
   
!*******************************************************************************
! store day, amount, and year of event ie
! set days of event to missing
!*******************************************************************************

  event(ie)=kD
  amount(ie)=rMax
  yearcount(lYr(kD))=yearcount(lYr(kD))+1

  do jD=kD,kD+DURATION-1
  rGrid(jD) = rMiss
  enddo

  enddo
  
  write(40,50)iLong,iLat,RETURN,DURATION,iNEV,(lYr(event(ie)),kD(event(ie)),amount(ie),ie=1,iNEV)
  50 format(5i5,221(2i6,f8.2))
  write(41,55)iLong,iLat,RETURN,DURATION,(iY,yearcount(iY),iY=BegYear,EndYear)
  55 format(4i5,221(2i5))
 

! END GRID POINT PROCESSING CODE

enddo
enddo

end program getprcpextremes
