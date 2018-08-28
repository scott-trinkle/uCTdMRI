function cartop2,fxy, NR = nr, NT = nt, CENTER = center

  dims = size(fxy, /dimensions)

  ;; dims = 10096  6720
  
if(n_elements(dims) ne 2) then message,"fxy not a 2D array"

if(~keyword_set(nr)) then nr = dims[0]  ;; 10096
if(~keyword_set(nt)) then nt = dims[0]  ;; 10096

if(~keyword_set(center)) then begin
  x0 = dims[0]/2. - .5 ;; 5047.5
  y0 = dims[1]/2. - .5 ;; 3359.5
endif else begin
  x0 = center[0]
  y0 = center[1]
endelse

r = (findgen(nr)+1)/float(nr)*x0 ;; = 0.4, 0.8, 1.2, 1.6, 2 for nr = 5
t = 2.*!pi*findgen(nt)/float(nt-1) ;; 0, 0.5pi, pi, 1.5pi, 2pi for nt = 5


xpolar=x0+r#cos(t) ;; dimension is 10096x10096
ypolar=y0+r#sin(t) ;; ypolar[0, 5] = y0 + r[0] * sin(t[5])

;
;
;
; - - since xpolar, ypolar not on a regular xy grid, can't use /grid keyword
; - - in interpolate.
;
frt=interpolate(fxy,xpolar,ypolar,cubic=-0.5) ;; 10096x1009648877
;
return, frt

end
