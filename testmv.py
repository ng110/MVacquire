import numpy as np

print "pre import"
import mv
print "post import"

l = mv.List(0)
for s in l.Devices.VD000001:#info without opening device
    print "%-25s: %s"%(s.name, s)

#dev = mv.dmg.get_device('BF004672')
#dev2 = mv.dmg.BF004672
#assert dev is dev2

dev = mv.dmg.get_device('VD000001')
settings = dev.Setting
cam_settings = settings.get_object_by_name('Camera')
#for s in cam_settings:
#    print "%-25s: %s"%(s.name, s)
    
#s = cam_settings['FlashMode']
#print s.get_dict()
#print s

pf = cam_settings.PseudoFeatures
for p in pf:
    print "%-25s: %s"%(p.name, p)

print pf.Pseudo64BitIntProp
pf.Pseudo64BitIntProp = 10
print pf.Pseudo64BitIntProp

print pf.PseudoIntVectorProp
pf.PseudoIntVectorProp = 1,2,3
print pf.PseudoIntVectorProp

## get image
#create request control (optional)
rc  = dev.create_request_control('my request control')

#request image, get nr of used request object
nr_requested = dev.image_request() #rc_idx argument????

#wait for image, returns image request nr
image_result = dev.get_image(timeout = 1.0)

#get request result/state
#requ_res, requ_state = dev.image_request_result(nr)
print image_result.result, image_result.state

print image_result.info


#test for validity
#if requ_res:

#get buffer
buf = image_result.get_buffer()
print "got image", buf.shape, buf
img = np.asarray(buf)
del image_result

#cleanup
dev.delete_request_control('my request control')


#call
print "frame count before statistics reset: ", dev.Statistics.FrameCount
#dev.Statistics.ResetStatistics()
m = dev.Statistics.get_object_by_name('ResetStatistics@i')
m()
print "frame count after  statistics reset: ", dev.Statistics.FrameCount


import pylab as plt
plt.imshow(np.squeeze(img))
plt.show()


