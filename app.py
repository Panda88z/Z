import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- إعدادات الواجهة ---
st.set_page_config(page_title="الباندا الصغير - EGX Quantum", layout="wide")

# --- 1. القائمة الذهبية الكاملة (بدون اختصار) ---
STOCKS_DB = {
    # القياديات والقطاع المالي
    "التجاري الدولي": "COMI.CA", "طلعت مصطفى": "TMGH.CA", "فوري": "FWRY.CA", "بلتون": "BTEL.CA",
    "هيرميس": "HRHO.CA", "إي فاينانس": "EFIH.CA", "سي آي كابيتال": "CICH.CA", "أبوظبي الإسلامي": "ADIB.CA",
    "البركة": "SAUD.CA", "كريدي أجريكول": "CIEB.CA", "بنك فيصل ج": "FAIT.CA", "بنك فيصل د": "FAIT_u.CA",
    "قطر الوطني": "QNBA.CA", "قناة السويس": "CANA.CA", "التعمير والإسكان": "HDBK.CA", "المصري الخليجي": "EGBE.CA",
    "القلعة": "CCAP.CA", "بايونيرز": "PINV.CA", "أوراسكوم المالية": "OFH.CA", "أوراسكوم للاستثمار": "OIH.CA",
    
    # العقارات والإنشاءات
    "بالم هيلز": "PHDC.CA", "مدينة مصر": "MNHD.CA", "مصر الجديدة": "HELI.CA", "سوديك": "OCDI.CA",
    "إعمار مصر": "EMFD.CA", "أوراسكوم للتنمية": "ORHD.CA", "أوراسكوم للإنشاء": "ORAS.CA", "زهراء المعادي": "ZMID.CA",
    "الشمس للإسكان": "ELSH.CA", "المطورون العرب": "ARAB.CA", "عامر جروب": "AMER.CA", "المصريين للإسكان": "EHTP.CA",
    "تنمية للاستثمار": "ARVA.CA", "عتاقة": "ASIC.CA", "المتحدة للإسكان": "UNIT.CA",
    
    # الصناعة والطاقة والكيماويات
    "السويدي": "SWDY.CA", "حديد عز": "ESRS.CA", "أبوقير للأسمدة": "ABUK.CA", "موبكو": "MFOT.CA",
    "كيما": "EGCH.CA", "سيدي كرير": "SKPC.CA", "أموك": "AMOC.CA", "مصر للألومنيوم": "EGAL.CA",
    "عز السيراميك": "ECAP.CA", "النساجون": "ORWE.CA", "غاز مصر": "EGAS.CA", "طاقة عربية": "TAQA.CA",
    "الدلتا للسكر": "SUGR.CA", "مصر للكيماويات": "MICH.CA", "أسيك للتعدين": "ASCM.CA", "العربية للأسمنت": "ARCC.CA",
    "أسمنت سيناء": "SCEM.CA", "الحديد والصلب": "IRON.CA", "الالومنيوم العربية": "ALUM.CA", "كفر الزيات": "KZPC.CA",
    
    # الأغذية والدواء والخدمات
    "جهينة": "JUFO.CA", "إيديتا": "EFID.CA", "دومتي": "DOMT.CA", "عبور لاند": "OLFI.CA",
    "الشرقية للدخان": "EAST.CA", "جي بي أوتو": "AUTO.CA", "القاهرة للدواجن": "POUL.CA", "المنصورة للدواجن": "MPCO.CA",
    "أجواء": "AJWA.CA", "دايس": "DSCW.CA", "إيبيكو": "PHAR.CA", "راميدا": "RMDA.CA", "كليوباترا": "CLHO.CA",
    "سبيد ميديكال": "SPMD.CA", "ابن سينا": "ISPH.CA", "المصرية للاتصالات": "ETEL.CA", "راية": "RAYA.CA",
    "الإسكندرية للحاويات": "ALCN.CA", "القناة للتوكيلات": "CSAG.CA", "ماريديف": "MOIL.CA"
}

# --- 2. محرك التحليل الشامل (The Beast Engine) ---
def advanced_panda_engine(ticker, interval):
    try:
        df = yf.download(ticker, period="2y", interval=interval, progress=False)
        if df.empty: return None

        # أ- الزخم والسيولة
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['MFI'] = ta.mfi(df['High'], df['Low'], df['Close'], df['Volume'], length=14)
        
        # ب- الاتجاه (MACD)
        macd = ta.macd(df['Close'])
        df = pd.concat([df, macd], axis=1)

        # ج- البولينجر (Bollinger)
        bb = ta.bbands(df['Close'], length=20, std=2)
        df = pd.concat([df, bb], axis=1)

        # د- فيبوناتشي (Fibonacci Levels)
        highest = df['High'].max()
        lowest = df['Low'].min()
        diff = highest - lowest
        df['Fib_618'] = highest - (0.618 * diff)
        df['Fib_382'] = highest - (0.382 * diff)

        # هـ- مدرسة جان الزمنية (Gann Geometry)
        df['Gann_Angle'] = lowest + (np.arange(len(df)) * (diff / len(df)))

        # و- ترقيم إليوت (Elliott Wave AI)
        df['SMA_50'] = ta.sma(df['Close'], length=50)
        df['Wave'] = np.where(df['Close'] > df['SMA_50'], "موجة 3 (صعود)", "موجة 4 أو 2 (تصحيح)")

        return df
    except:
        return None

# --- 3. الواجهة والمساعد الشخصي ---
st.title("🐼 الباندا الصغير v21.0 | الإمبراطور")
st.sidebar.header("🤵 مساعد المحفظة الشخصي")

with st.sidebar.expander("💼 حلل أرباحي وقراري"):
    my_stk = st.selectbox("سهمك:", list(STOCKS_DB.keys()))
    my_prc = st.sidebar.number_input("سعر دخولك:", value=0.0)
    if st.sidebar.button("ماذا أفعل الآن؟"):
        d = advanced_panda_engine(STOCKS_DB[my_stk], "1d")
        if d is not None:
            curr = d['Close'].iloc[-1]
            gain = ((curr - my_prc) / my_prc) * 100
            st.write(f"النتيجة الحالية: {gain:.2f}%")
            if gain < -7: st.error("🛑 السهم خطر! اخرج بوقف خسارة فوراً.")
            elif gain > 15: st.success("💰 رابح جداً! جني أرباح جزئي.")
            else: st.info("⏳ السعر مستقر، استمر في المراقبة.")

# --- 4. الرادار العميق ---
selected = st.sidebar.selectbox("اختر السهم من رادار الباندا:", list(STOCKS_DB.keys()))
tf = st.sidebar.radio("فريم التحليل:", ("يومي", "ساعة"))
interval = "1d" if "يومي" in tf else "1h"

if st.sidebar.button("شغل الرادار النووي"):
    data = advanced_panda_engine(STOCKS_DB[selected], interval)
    if data is not None:
        l = data.iloc[-1]
        
        # كروت الأداء
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("السعر", f"{l['Close']:.2f}")
        col2.metric("السيولة MFI", f"{l['MFI']:.1f}")
        col3.metric("الزخم RSI", f"{l['RSI']:.1f}")
        col4.metric("الموجة الحالية", l['Wave'])

        # تحليل المدارس
        st.markdown("---")
        c_left, c_right = st.columns(2)
        
        with c_left:
            st.subheader("⏳ تحليل جان وفيبوناتشي")
            st.write(f"📐 زاوية جان الحالية: {l['Gann_Angle']:.2f}")
            st.write(f"📍 دعم فيبوناتشي (61.8%): {l['Fib_618']:.2f}")
            st.write(f"📍 مقاومة فيبوناتشي (38.2%): {l['Fib_382']:.2f}")
            
        with c_right:
            st.subheader("🎯 مناطق الدخول والخروج")
            st.success(f"✅ أفضل سعر دخول: {l['BBL_20_2.0']:.2f}")
            st.error(f"⚠️ منطقة جني الأرباح: {l['BBU_20_2.0']:.2f}")
            if l['Close'] < l['BBL_20_2.0']: st.warning("السهم الآن في فرصة دخول تاريخية!")

        st.line_chart(data[['Close', 'BBL_20_2.0', 'BBU_20_2.0', 'Gann_Angle']])
    else:
        st.error("فشل جلب البيانات.")
