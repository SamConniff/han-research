const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');const path=require('path');
const D=__dirname; const men=fs.readFileSync(D+'/men.json','utf8');
fs.writeFileSync(D+'/_built.html',fs.readFileSync(D+'/'+(process.env.SRC||'reel.html'),'utf8').replace('__MEN__',men));
const fps=+(process.env.FPS||30); const only=process.argv.slice(2); const out=process.env.OUT||'out.mp4';
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const pg=await b.newPage({viewport:{width:1080,height:1920}});
 await pg.goto('file://'+D+'/_built.html'); await pg.evaluate('window.READY'); await pg.waitForTimeout(800); await pg.evaluate('render(0)');
 const st=pg.locator('#stage');
 if(only.length){for(const s of only){await pg.evaluate(`render(${s})`);await st.screenshot({path:`${D}/still_${s}.png`})}}
 else{const dur=await pg.evaluate('DURATION');const n=Math.round(dur*fps);
  const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',''+fps,'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-movflags','+faststart',D+'/'+out],{stdio:['pipe','inherit','inherit']});
  for(let i=0;i<n;i++){await pg.evaluate(`render(${i/fps})`);const buf=await st.screenshot({type:'jpeg',quality:94});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r))}
  ff.stdin.end();await new Promise(r=>ff.on('close',r))}
 await b.close()})();
