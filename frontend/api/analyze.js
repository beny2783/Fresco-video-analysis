import { NextRequest, NextResponse } from 'next/server';

// Note: This is a simplified version for Vercel serverless functions
// Due to Vercel's limitations (10s timeout, 50MB payload), this may not work for large videos
export async function POST(request) {
  try {
    const formData = await request.formData();
    const file = formData.get('file');
    
    if (!file) {
      return NextResponse.json(
        { status: 'error', error: 'No file provided' },
        { status: 400 }
      );
    }

    // Check file size (Vercel has 50MB limit for serverless functions)
    const fileSize = file.size;
    if (fileSize > 50 * 1024 * 1024) {
      return NextResponse.json(
        { status: 'error', error: 'File too large. Maximum size is 50MB.' },
        { status: 400 }
      );
    }

    // Convert file to buffer
    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    // For now, return a placeholder response
    // In a real implementation, you would need to:
    // 1. Use a different approach for Google Gemini API (serverless compatible)
    // 2. Handle the video processing differently
    // 3. Consider using external services for video processing
    
    return NextResponse.json({
      status: 'success',
      message: 'Video analysis endpoint ready. Backend deployment required for full functionality.',
      fileSize: fileSize,
      fileName: file.name
    });

  } catch (error) {
    console.error('Error processing video:', error);
    return NextResponse.json(
      { status: 'error', error: error.message },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    status: 'success',
    message: 'Video analysis API endpoint'
  });
} 