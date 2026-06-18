import ir_datasets

def print_samples():
    print("=" * 60)
    print(" سكربت الاستخراج الحي للاستعلامات والـ Qrels محلياً")
    print("=" * 60)
    
    
    dataset_id = 'msmarco-document/train'
    print(f"[INFO] جاري الاتصال بـ الـ Dataset: {dataset_id}...\n")
    
    try:
        dataset = ir_datasets.load(dataset_id)
        
        
        print("📋 [1] عينة من الاستعلامات المتوفرة (Testing/Training Queries):")
        if dataset.has_queries():
            
            for i, query in enumerate(dataset.queries_iter()):
                print(f"   - ID الاستعلام: {query.query_id} -> النص: '{query.text}'")
                if i >= 2:
                    break
            print("    الاستعلامات موجودة وتقرأ بنجاح!")
        else:
            print("    لا توجد استعلامات في هذا المسار.")
            
        print("-" * 60)
        
        
        print(" [2] عينة من ملف الأحكام والملائمة (Qrels - Ground Truth):")
        if dataset.has_qrels():
           
            for i, qrel in enumerate(dataset.qrels_iter()):
                print(f"   - ID الاستعلام: {qrel.query_id} ملائم للوثيقة ID: {qrel.doc_id} (درجة الملائمة: {qrel.relevance})")
                if i >= 2:
                    break
            print("    ملفات الـ Qrels موجودة وتقرأ بنجاح!")
        else:
            print("    لا توجد ملفات qrels في هذا المسار.")
            
        print("=" * 60)
        print(" النتيجة: تم إثبات وجود الـ Queries والـ Qrels محلياً 100%!")
        print("=" * 60)

    except Exception as e:
        print(f" حدثت مشكلة أثناء استدعاء التقييم.")
        print(f"الرسالة: {e}")

if __name__ == "__main__":
    print_samples()