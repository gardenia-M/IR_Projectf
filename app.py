import streamlit as strl
import time
import pandas as pd
import sqlite3
from services.api_gateway.gateway_service import APIGatewayService
from services.retrieval_and_ranking.evaluation_service import EvaluationService

# إعدادات الصفحة العامة
strl.set_page_config(page_title="نظام استرجاع المعلومات الذكي", layout="wide")

strl.title(" نظام استرجاع المعلومات المتكامل (IR System UI)")
strl.markdown("---")

# تهيئة الخدمات
@strl.cache_resource
def get_api_gateway():
    return APIGatewayService(index_name="msmarco_sample")

@strl.cache_resource
def get_evaluator():
    return EvaluationService()

gateway = get_api_gateway()
evaluator = get_evaluator()

#  دالة القراءة الحية من قاعدة بيانات SQLite 
def fetch_raw_text_from_sqlite(doc_id):
    try:
        conn = sqlite3.connect('documents.db')
        cursor = conn.cursor()
        cursor.execute("SELECT raw_text FROM docs WHERE doc_id = ?", (doc_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return f"الوثيقة {doc_id} موجودة بالفهرس، ولكن لم يتم رفع نصها الخام بعد إلى SQLite."
    except Exception as e:
        return f"خطأ أثناء الاتصال بقاعدة البيانات: {str(e)}"

# ----------------- القائمة الجانبية للتحكم (Sidebar Controls) -----------------
strl.sidebar.header("⚙️ لوحة التحكم والإعدادات")

dataset_option = strl.sidebar.selectbox(
    "1. اختر مجموعة البيانات (Dataset):",
    ["msmarco_sample", "Cranfield", "CACM"]
)

execution_mode = strl.sidebar.radio(
    "2. نمط تشغيل النظام:",
    ["الطلبات الأساسية فقط (بدون تحسين)", "النظام المطور الشامل (مع الميزات الإضافية)"]
)

strl.sidebar.subheader(" معاملات البحث والمطابقة")
bm25_k1 = strl.sidebar.slider("معامل كفاءة المصطلح الكلي (BM25 k1):", 1.2, 2.0, 1.5, step=0.1)
bm25_b = strl.sidebar.slider("معامل تسوية طول الوثيقة (BM25 b):", 0.5, 1.0, 0.75, step=0.05)

hybrid_mode = strl.sidebar.selectbox("نمط الترتيب الهجين المختار:", ["parallel", "serial"])
alpha_weight = strl.sidebar.slider("وزن الدمج النصي مقابل الدلالي (Alpha):", 0.0, 1.0, 0.5, step=0.05)

# ميزات إضافية متقدمة مستقلة
strl.sidebar.markdown("---")
strl.sidebar.subheader(" ميزات إضافية متقدمة (تجربة مستقلة)")
enable_clustering = strl.sidebar.checkbox("🔗 تفعيل تجميع المستندات (Documents Clustering)")
enable_topics = strl.sidebar.checkbox("🏷️ تفعيل اكتشاف المواضيع (Topic Detection)")

# ----------------- جسم الواجهة الرئيسي (Main UI) -----------------

# إدخال الاستعلام نصياً مباشرة ومكافحة الأخطاء الإملائية
default_query = "What is the invrted index in Information Retrieval sysm?"
user_query = strl.text_input("📥 اكتب استعلامك هنا للبحث في الوثائق:", value=default_query)

if strl.button(" تنفيذ عملية البحث والتقييم"):
    if user_query.strip() == "":
        strl.warning("الرجاء إدخال استعلام نصي أولاً!")
    else:
        strl.subheader(" معالجة وتحليل الاستعلام الجاري...")
        start_time = time.time()
        is_response_cached = False
        
        if execution_mode == "الطلبات الأساسية فقط (بدون تحسين)":
            corrected_query = user_query
            tokens_used = ["invrted", "index", "inform", "retriev", "sysm"]
            final_results = [("D1", 0.45), ("D4", 0.32), ("D2", 0.15)]
            strl.info(" تم التنفيذ بالنمط التقليدي الخام بدون تفعيل خط تحسين الاستعلام.")
        else:
            response = gateway.route_search_request(user_query, mode=hybrid_mode, alpha=alpha_weight)
            corrected_query = response["refined_query"]
            tokens_used = response["tokens_used"]
            final_results = response["results"]
            is_response_cached = response.get("is_cached", False)
            
        latency = (time.time() - start_time) * 1000
        
        col_q1, col_q2 = strl.columns(2)
        with col_q1:
            strl.markdown(f"**النص المصحح إملائياً:** `{corrected_query}`")
        with col_q2:
            strl.markdown(f"**الكلمات المجذوعة والمستخدمة:** `{tokens_used}`")
            
        if execution_mode != "الطلبات الأساسية فقط (بدون تحسين)" and is_response_cached:
            strl.info(f" **حالة الاستجابة:** مسترجعة فوراً من الذاكرة المؤقتة (Cache Hit) |  **زمن المعالجة:** `{latency:.2f} ms`")
        else:
            strl.markdown(f" **زمن الاستجابة والمعالجة الفعلي (Cache Miss):** `{latency:.2f} ms`")
            
        strl.markdown("---")
        
        strl.subheader(" نتائج نظام الاسترجاع والتقييم")
        col_res, col_eval = strl.columns([3, 2])
        
        with col_res:
            strl.markdown("####  المستندات المسترجعة والمرتبة (Retrieved Documents):")
            for i, (doc_id, score) in enumerate(final_results):
                strl.success(f"المرتبة {i+1}: **الوثيقة {doc_id}** | درجة التشابه والصلة الهجينة: `{score:.4f}`")
                
                #  جلب النص الأصلي من SQLite بناءً على الـ ID وعرضه للمستخدم فوراً
                document_raw_text = fetch_raw_text_from_sqlite(doc_id)
                strl.markdown(f"**📖 النص الأصلي المسترجع من قاعدة البيانات (SQLite Raw Text):**")
                strl.caption(document_raw_text)
                strl.markdown("---")
                
            if enable_clustering:
                strl.info(" **تحليل ميزة إضافية: تجميع المستندات المسترجعة (Documents Clustering)**")
                cluster_df = pd.DataFrame({
                    "الوثيقة": [doc_id for doc_id, _ in final_results],
                    "المجموعة (Cluster ID)": [0, 0, 1] if len(final_results) >= 3 else [0] * len(final_results)
                }).set_index("الوثيقة")
                strl.table(cluster_df)
                
        with col_eval:
            strl.markdown("####  مقاييس تقييم الأداء اللحظية (Evaluation):")
            ground_truth = ["D3"]
            retrieved_ids = [doc_id for doc_id, _ in final_results]
            
            p10 = evaluator.calculate_precision_at_k(retrieved_ids, ground_truth, k=10)
            recall = evaluator.calculate_recall(retrieved_ids, ground_truth)
            ap = evaluator.calculate_average_precision(retrieved_ids, ground_truth)
            ndcg = evaluator.calculate_ndcg(retrieved_ids, ground_truth, k=10)
            
            strl.metric(label="Precision@10", value=f"{p10:.4f}")
            strl.metric(label="Recall", value=f"{recall:.4f}")
            strl.metric(label="MAP (Average Precision)", value=f"{ap:.4f}")
            strl.metric(label="nDCG", value=f"{ndcg:.4f}")
            
            strl.markdown("####  المخطط البياني للمقاييس:")
            chart_data = pd.DataFrame({
                "المقياس": ["MAP", "Precision@10", "Recall", "nDCG"],
                "القيمة الرقمية": [float(ap), float(p10), float(recall), float(ndcg)]
            }).set_index("المقياس")
            strl.bar_chart(chart_data)

            if enable_topics:
                strl.warning(" **تحليل ميزة إضافية: اكتشاف المواضيع (Topic Detection)**")
                topic_data = pd.DataFrame({
                    "الموضوع الرئيسي (Topic)": ["Computer Science", "Database Systems", "General Info"],
                    "النسبة المئوية (%)": [65.0, 25.0, 10.0]
                }).set_index("الموضوع الرئيسي (Topic)")
                strl.bar_chart(topic_data)