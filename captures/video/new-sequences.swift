import Foundation
import AVFoundation
import AppKit
import CoreImage
let files = [
("5327", "/private/var/folders/22/h4v_r9bn5wsgf7s7mxkp7gs40000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=E4A41943-1986-4C22-A5D5-0BD667DD89C5&code=001&library=1&type=3&mode=2&loc=true&cap=true.mov/IMG_5327.mov"),
("5328", "/private/var/folders/22/h4v_r9bn5wsgf7s7mxkp7gs40000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=0D2DB2FF-2017-4999-83BC-38BD482424FB&code=001&library=1&type=3&mode=2&loc=true&cap=true.mov/IMG_5328.mov")]
let positions: [String:[(Int,Int)]] = [
"5327":[(620,60),(749,68),(839,156),(848,255),(812,350),(742,411),(568,407),(500,342),(479,247),(511,141)],
"5328":[(584,65),(715,69),(805,146),(829,250),(803,345),(735,407),(559,409),(490,348),(458,253),(485,151)]]
let ciContext = CIContext()
for (name,path) in files {
 let asset=AVURLAsset(url:URL(fileURLWithPath:path))
 let track=asset.tracks(withMediaType:.video).first!
 print("Track \(name): transform \(track.preferredTransform)")
 let reader=try! AVAssetReader(asset:asset)
 let output=AVAssetReaderTrackOutput(track:track,outputSettings:[kCVPixelBufferPixelFormatTypeKey as String:kCVPixelFormatType_32BGRA])
 output.alwaysCopiesSampleData=false
 reader.add(output); reader.startReading()
 var lines=["time,"+(0..<10).map{"L\($0)"}.joined(separator:",")]
 var n=0
 while let sample=output.copyNextSampleBuffer() {
  autoreleasepool {
   let t=CMTimeGetSeconds(CMSampleBufferGetPresentationTimeStamp(sample))
   guard let pb=CMSampleBufferGetImageBuffer(sample) else {return}
   let source=CIImage(cvPixelBuffer:pb)
   let resized=source.transformed(by:CGAffineTransform(scaleX:450.0/source.extent.width,y:450.0/source.extent.width))
   guard let cg=ciContext.createCGImage(resized,from:resized.extent) else {return}
   let w=cg.width,h=cg.height
   var pixels=[UInt8](repeating:0,count:w*h*4)
   pixels.withUnsafeMutableBytes {ptr in
    let ctx=CGContext(data:ptr.baseAddress,width:w,height:h,bitsPerComponent:8,bytesPerRow:w*4,space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.draw(cg,in:CGRect(x:0,y:0,width:w,height:h))
   }
   var counts=[Int]()
   for (xx,yy) in positions[name]! {
    let cx=xx/2,cy=yy/2
    var count=0
    for y in max(0,cy-20)..<min(h,cy+21) {for x in max(0,cx-20)..<min(w,cx+21) {
     let p=(y*w+x)*4,r=Int(pixels[p]),g=Int(pixels[p+1]),b=Int(pixels[p+2])
     if g>160 && g-r>40 && g-b>12 {count+=1}
    }}
    counts.append(count)
   }
   lines.append(String(format:"%.5f",t)+","+counts.map{String($0)}.joined(separator:","))
   if n==300 {
    let rep=NSBitmapImageRep(cgImage:cg)
    try! rep.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:"captures/video/\(name)-reader-check.png"))
   }
   n+=1
  }
 }
 try! lines.joined(separator:"\n").write(toFile:"captures/video/\(name)-led-counts.csv",atomically:true,encoding:.utf8)
 print("Decoded \(name): \(n) frames; reader status \(reader.status.rawValue), error \(String(describing:reader.error))")
}
