

# Act on these classes of drugs
#
dictAllDrugClasses = {
    'Ace Inhibitors': {
        'drugs': ['Benazepril','Captopril','Enalapril','Enalaprilat','Fosinopril','Lisinopril','Moexipril','Perindopril','Quinapril','Ramipril','Trandolapril'] ,
        'desc': 'Lower blood pressure'
    },
    'ADHD Treatments': {
        'drugs': ['Atomoxetine','Guanfacine','Lisdexamfetamine','Methylphenidate'],
        'desc': 'Treat ADHD'
    },
    'Aldosterone Antagonists': {
        'drugs': ['Eplerenone','Finerenone','Spironolactone'],
        'desc': 'Diuretic'
    },
    'Alpha2 Andrenergic Agonist Hypertension': {
        'drugs': ['Azilsartan medoxomil','Candesartan cilexetil','Eprosartan','Irbesartan','Losartan','Olmesartan','Telmisartan','Valsartan'], 
        'desc': 'Lower blood pressure'
    },
    'Angiotensin II Receptor Blockers': {
        'drugs': ['Azilsartan medoxomil','Candesartan cilexetil','Eprosartan','Irbesartan','Losartan','Olmesartan','Telmisartan','Valsartan'],
        'desc': 'Lower blood pressure'
    },
    'Antiarrhythmics': {
        'drugs': ['Amiodarone','Flecainide','Procainamide','Propafenone','Quinidine','Sotalol','Tocainide'],
        'desc': 'Treat arrythmias'
    },
    'Antiarrhythmic IVs': {
        'drugs': ['Ibutilide','Lidocaine'],
        'desc': 'Treat arrythmias by IV'
	},
    'Antibiotics Common': {
        'drugs': ['Amoxicillin','Azithromycin','Cephalexin','Ciprofloxacin','Clarithromycin','Clindamycin','Doxycycline','Levofloxacin',
            'Metronidazole','Trimethoprim','Vancomycin'],
        'desc': 'Common antibiotics'
	},
    'Beta Adrenergic Blocking Agents': {
        'drugs': ['Nadolol','Oxprenolol','Pindolol','Propranolol','Penbutolol','Timolol'],
        'desc': 'Lower blood pressure'
	},
    'Bisphosphonates': {
        'drugs': ['Alendronic acid','Etidronic acid','Ibandronate','Pamidronic acid','Risedronic acid','Zoledronic acid'],
        'desc': 'Treat osteoporosis'
	},
    'Bronchodilators': {
        'drugs': ['Aclidinium','Arformoterol','Formoterol','Indacaterol','Ipratropium','Salmeterol','Theophylline','Tiotropium'],
        'desc': 'Treat asthma and COPD'
	},
    'CCB Dihydropyridines': {
        'drugs': ['Amlodipine','Clevidipine','Felodipine','Isradipine','Nicardipine','Nifedipine','Nimodipine','Nisoldipine'],
        'desc': 'Lower blood pressure'
	},
    'CCB nonDihydropyridines': {
        'drugs': ['Diltiazem','Verapamil'],
        'desc': 'Lower blood pressure'
	},
    'Direct Vasodilators': {
        'drugs': ['Hydralazine','Minoxidil','Nitroglycerin'],
        'desc': 'Treat severe hypertension'
	},
    'Estrogen Modulators': {
        'drugs': ['Bazedoxifene','Ospemifene','Raloxifene','Toremifene'],
        'desc': 'Treat breast cancer and osteoporosis'
	},
    'Glaucoma Treatments': {
        'drugs': ['Apraclonidine','Bimatoprost','Brimonidine','Brinzolamide','Dipivefrin','Dorzolamide','Latanoprost',
            'Latanoprostene bunod','Pilocarpine','Tafluprost','Timolol','Travoprost'],
        'desc': 'Treat glaucoma'
	},
    'H2 Receptor Antagonists': {
        'drugs': ['Cimetidine','Famotidine','Ranitidine'],
        'desc': 'Treat gastric ulcers, reflux and heartburn'
	},
    'Hormonal Chemotherapy': {
        'drugs': ['Abemaciclib','Anastrozole','Exemestane','Fulvestrant','Goserelin','Letrozole','Leuprolide','Megestrol acetate','Tamoxifen'],
        'desc': 'Cancer treatment'
	},
    'Insulins': {
        'drugs': ['Insulin aspart','Insulin beef','Insulin degludec','Insulin detemir','Insulin glargine','Insulin glulisine',
            'Insulin human','Insulin lispro','Insulin pork'],
        'desc': 'Diabetes treatment'
	},
    'Loop Diuretics': {
        'drugs': ['Bumetanide','Etacrynic acid','Furosemide','Torasemide'],
        'desc': 'Diuretic'
	},
    'Macular Degeneration Treaments': {
        'drugs': ['Bevacizumab','Brolucizumab','Pentosan polysulfate','Ranibizumab','Verteporfin'],
        'desc': 'Macular degeneration treatment'
	},
    'Neuraminidase Inhibitors': {
        'drugs': ['Oseltamivir', 'Peramivir', 'Zanamivir'],
        'desc': 'Treat influenza'
	},
    'NSAIDs': {
        'drugs': ['Acetylsalicylic acid','Celecoxib','Diclofenac','Etoricoxib','Ibuprofen','Indomethacin','Mefenamic acid','Naproxen'],
        'desc': 'Non-steroidal anti-inflammatories'
	},
    'Potassium Sparing Diuretics': {
        'drugs': ['Amiloride','Eplerenone','Spironolactone','Triamterene'],
        'desc': 'Diuretic'
	},
    'Proton Pump Inhibitors': {
        'drugs': ['Dexlansoprazole','Esomeprazole','Lansoprazole','Omeprazole','Pantoprazole','Rabeprazole'],
        'desc': 'Stomach acid treatment (PPI)'
	},
    'Psoriasis': {
        'drugs':['Adalimumab','Apremilast','Etanercept','Guselkumab','Infliximab','Ixekizumab','Secukinumab','Tildrakizumab','Triamcinolone','Ustekinumab'] ,
        'desc': 'Psoriasis treatment'
	},
    'Reproductive Hormones': {
        'drugs': ['Estradiol','Estrone','Progesterone','Testosterone'],
        'desc': 'Reproductive hormones'
	},
    'Selective Beta1 Antagonist Agents': {
        'drugs': ['Acebutolol','Atenolol','Betaxolol','Bisoprolol','Carvedilol','Esmolol','Labetalol','Metoprolol','Nebivolol'],
        'desc': 'Lower blood pressure'
	},
    'SSRIs': {
        'drugs': ['Citalopram','Escitalopram','Fluoxetine','Paroxetine','Sertraline'], 
        'desc': 'Antidepressant'
	},
    'Statins': {
        'drugs': ['Atorvastatin','Fluvastatin','Lovastatin','Pravastatin','Rosuvastatin','Simvastatin'],
        'desc': 'Lower cholesterol'
	},
    'Thiazide Diuretics': {
        'drugs': ['Chlorthalidone','Chlorothiazide','Hydrochlorothiazide','Indapamide','Metolazone'],
        'desc': 'Diuretic'
	},
    'Thyroid Hormones': {
        'drugs': ['Levothyroxine','Liothyronine','Liotrix','Thyrotropin alfa'],
        'desc': 'Treat hypothyroidism'
	}
}
