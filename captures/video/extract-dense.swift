import Foundation
import AVFoundation
import AppKit
let files = [
("5318", "/private/var/folders/22/h4v_r9bn5wsgf7s7mxkp7gs40000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=81CDB7F3-8E01-4B31-ACD3-4A24CC1EBBF1&code=001&library=1&type=3&mode=2&loc=true&cap=true.mov/IMG_5318.mov"),
("5316", "/private/var/folders/22/h4v_r9bn5wsgf7s7mxkp7gs40000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=DED238D2-FD4F-44EA-8DC6-5C1648B5F765&code=001&library=1&type=3&mode=2&loc=true&cap=true.mov/IMG_5316.mov")]
for (name,path) in files {
 let asset = AVURLAsset(url: URL(fileURLWithPath:path))
 let duration = CMTimeGetSeconds(asset.duration)
 let gen = AVAssetImageGenerator(asset:asset)
 gen.appliesPreferredTrackTransform=true
 gen.maximumSize=CGSize(width:900,height:900)
 gen.requestedTimeToleranceBefore = .zero
 gen.requestedTimeToleranceAfter = .zero
 print("VIDEO \(name) duration \(duration)")
 for sec in stride(from:0.0,to:duration,by:0.25) {
  do {
   var actual=CMTime.zero
   let cg=try gen.copyCGImage(at:CMTime(seconds:sec,preferredTimescale:600),actualTime:&actual)
   let rep=NSBitmapImageRep(cgImage:cg)
   let data=rep.representation(using:.png,properties:[:])!
   let out=String(format:"captures/video/dense-%@-%05d.png",name,Int(sec*100))
   try data.write(to:URL(fileURLWithPath:out))
  } catch { print(error) }
 }
}
