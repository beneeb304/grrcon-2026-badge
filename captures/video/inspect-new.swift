import Foundation
import AVFoundation
import AppKit
let files = [
("5327", "/private/var/folders/22/h4v_r9bn5wsgf7s7mxkp7gs40000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=E4A41943-1986-4C22-A5D5-0BD667DD89C5&code=001&library=1&type=3&mode=2&loc=true&cap=true.mov/IMG_5327.mov"),
("5328", "/private/var/folders/22/h4v_r9bn5wsgf7s7mxkp7gs40000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=0D2DB2FF-2017-4999-83BC-38BD482424FB&code=001&library=1&type=3&mode=2&loc=true&cap=true.mov/IMG_5328.mov")]
for (name,path) in files {
 let asset = AVURLAsset(url: URL(fileURLWithPath:path))
 let duration = CMTimeGetSeconds(asset.duration)
 let gen = AVAssetImageGenerator(asset:asset)
 gen.appliesPreferredTrackTransform=true
 gen.maximumSize=CGSize(width:900,height:900)
 gen.requestedTimeToleranceBefore = .zero
 gen.requestedTimeToleranceAfter = .zero
 print("VIDEO \(name) duration \(duration) track \(asset.tracks(withMediaType:.video).first!.naturalSize) fps \(asset.tracks(withMediaType:.video).first!.nominalFrameRate)")
 for sec in [0.0, 2.0, 5.0, 10.0, 20.0, 30.0, 45.0, 60.0] where sec < duration {
  do {
   var actual=CMTime.zero
   let cg=try gen.copyCGImage(at:CMTime(seconds:sec,preferredTimescale:600),actualTime:&actual)
   let rep=NSBitmapImageRep(cgImage:cg)
   let data=rep.representation(using:.png,properties:[:])!
   let out=String(format:"captures/video/%@-%03d.png",name,Int(sec))
   try data.write(to:URL(fileURLWithPath:out))
  } catch { print(error) }
 }
}
