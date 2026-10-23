import AppKit
import AVFoundation
import CoreVideo

struct Page: Decodable { let title: String; let text: String }
let directory = URL(fileURLWithPath: CommandLine.arguments[1])
let pages = try JSONDecoder().decode([Page].self, from: Data(contentsOf: directory.appendingPathComponent("pages.json")))
let target = directory.appendingPathComponent("travel-demo.mp4")
if FileManager.default.fileExists(atPath: target.path) { try FileManager.default.removeItem(at: target) }
let width = 1440, height = 900
let writer = try AVAssetWriter(outputURL: target, fileType: .mp4)
let input = AVAssetWriterInput(mediaType: .video, outputSettings: [AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: width, AVVideoHeightKey: height])
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input, sourcePixelBufferAttributes: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB, kCVPixelBufferWidthKey as String: width, kCVPixelBufferHeightKey as String: height, kCVPixelBufferCGImageCompatibilityKey as String: true, kCVPixelBufferCGBitmapContextCompatibilityKey as String: true])
writer.add(input)
guard writer.startWriting() else { fatalError("Video writer failed") }
writer.startSession(atSourceTime: .zero)
let bodyFont = NSFont(name: "Apple SD Gothic Neo", size: 27) ?? NSFont.systemFont(ofSize: 27)
func draw(_ text: String, _ rect: NSRect, _ font: NSFont, _ color: NSColor) {
    let style = NSMutableParagraphStyle(); style.lineSpacing = 6
    (text as NSString).draw(in: rect, withAttributes: [.font: font, .foregroundColor: color, .paragraphStyle: style])
}
var index: Int64 = 0
for (pageIndex, page) in pages.enumerated() {
    var optionalBuffer: CVPixelBuffer?
    CVPixelBufferCreate(kCFAllocatorDefault, width, height, kCVPixelFormatType_32ARGB, nil, &optionalBuffer)
    guard let buffer = optionalBuffer else { fatalError("Buffer allocation failed") }
    CVPixelBufferLockBaseAddress(buffer, [])
    let context = CGContext(data: CVPixelBufferGetBaseAddress(buffer), width: width, height: height, bitsPerComponent: 8, bytesPerRow: CVPixelBufferGetBytesPerRow(buffer), space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(cgContext: context, flipped: false)
    NSColor(calibratedRed: 0.055, green: 0.075, blue: 0.11, alpha: 1).setFill()
    NSRect(x: 0, y: 0, width: width, height: height).fill()
    draw("●  ●  ●    travel-recommender", NSRect(x: 40, y: 838, width: 1300, height: 40), NSFont.monospacedSystemFont(ofSize: 23, weight: .regular), .lightGray)
    draw(page.title, NSRect(x: 48, y: 770, width: 1344, height: 55), NSFont.systemFont(ofSize: 34, weight: .bold), NSColor(calibratedRed: 0.35, green: 0.85, blue: 0.7, alpha: 1))
    draw(page.text, NSRect(x: 48, y: 70, width: 1344, height: 690), bodyFont, .white)
    draw("실제 로그·리포트 기반 영상 | 화면 촬영 아님    \(pageIndex + 1) / \(pages.count)", NSRect(x: 48, y: 15, width: 1344, height: 35), NSFont.systemFont(ofSize: 19), .lightGray)
    NSGraphicsContext.restoreGraphicsState()
    CVPixelBufferUnlockBaseAddress(buffer, [])
    for _ in 0..<10 {
        while !input.isReadyForMoreMediaData { Thread.sleep(forTimeInterval: 0.01) }
        guard adaptor.append(buffer, withPresentationTime: CMTime(value: index, timescale: 1)) else { fatalError("Frame append failed") }
        index += 1
    }
}
writer.endSession(atSourceTime: CMTime(value: index, timescale: 1))
input.markAsFinished()
let semaphore = DispatchSemaphore(value: 0)
writer.finishWriting { semaphore.signal() }
semaphore.wait()
guard writer.status == .completed else { fatalError("Encoding failed: \(String(describing: writer.error))") }
print("MP4 생성 완료: \(target.path), \(index)초")
