import Foundation
import AVFoundation
import AppKit
let files = [
("5318", "/private/var/folders/22/h4v_r9bn5wsgf7s7mxkp7gs40000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=81CDB7F3-8E01-4B31-ACD3-4A24CC1EBBF1&code=001&library=1&type=3&mode=2&loc=true&cap=true.mov/IMG_5318.mov"),
("5316", "/private/var/folders/22/h4v_r9bn5wsgf7s7mxkp7gs40000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=DED238D2-FD4F-44EA-8DC6-5C1648B5F765&code=001&library=1&type=3&mode=2&loc=true&cap=true.mov/IMG_5316.mov")]
for (name,path) in files {
 let asset = AVURLAsset(url: URL(fileURLWithPath:path))
 let duration=CMTimeGetSeconds(asset.duration)
 let fps=asset.tracks(withMediaType:.video).first?.nominalFrameRate ?? 0
 print("VIDEO \(name) duration \(duration) nativeFPS \(fps)")
 let gen=AVAssetImageGenerator(asset:asset)
 gen.appliesPreferredTrackTransform=true
 gen.maximumSize=CGSize(width:450,height:450)
 gen.requestedTimeToleranceBefore = .zero
 gen.requestedTimeToleranceAfter = .zero
 var lines=["time,brightPixels"]
 for sec in stride(from:12.0,to:duration,by:1.0/30.0) {
  do {
   let cg=try gen.copyCGImage(at:CMTime(seconds:sec,preferredTimescale:600),actualTime:nil)
   let w=cg.width,h=cg.height
   var pixels=[UInt8](repeating:0,count:w*h*4)
   pixels.withUnsafeMutableBytes { ptr in
    let ctx=CGContext(data:ptr.baseAddress,width:w,height:h,bitsPerComponent:8,bytesPerRow:w*4,space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.draw(cg,in:CGRect(x:0,y:0,width:w,height:h))
   }
   var count=0
   for y in 0..<min(h,165) { for x in 190..<w {
    let p=(y*w+x)*4,r=Int(pixels[p]),g=Int(pixels[p+1]),b=Int(pixels[p+2])
    if g>170 && g-r>45 && g-b>15 {count+=1}
   }}
   lines.append(String(format:"%.4f,%d",sec,count))
  } catch {print(error);break}
 }
 try! lines.joined(separator:"\n").write(toFile:"captures/video/\(name)-30fps-brightness.csv",atomically:true,encoding:.utf8)
 print("Saved \(name): \(lines.count-1) samples")
}
