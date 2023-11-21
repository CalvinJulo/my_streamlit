from mlconjug3 import Conjugator


lang_list = ['fr', 'en', 'es', 'it', 'pt', 'ro']

conjugator = Conjugator(language='es')

def conjug_dict(verb):
    a = {}
    b = {}
    c = ['Infinitivo','Gerundio','Participo']
    d = []
    for i in verb.iterate():
        if i[0] in c:
            pass
        else:
            if i[1] not in d:
                d.append(i[1])
                if i[0] =='Imperativo':
                    b[i[1]] = ['–']
                else:
                    b[i[1]]=[]
            if i[1] in d:
                b[i[1]].append(i[3])
    for i in ['Infinitivo','Gerundio']:
        a1 = verb[i]
        for k1, v1 in a1.items():
            for k2, v2 in v1.items():
                a[k1] = [v2]
    for k, v in verb['Participo'].items():
        a[k] = [v]
    return a,b


def conjug_dfs(word):
    verb = conjugator.conjugate(word)
    verb_a, verb_b = conjug_dict(verb)
    verb_a_df = pd.DataFrame(verb_a).transpose()
    verb_a_df.columns = [verb_a_df.loc['Infinitivo Infinitivo',0]]
    verb_b_df = pd.DataFrame(verb_b).transpose()
    columns_names = ['yo','tú','él/ella/usted','nosotros/nosotras','vosotros/vosotras','ellos/ellas/ustedes']
    verb_b_df.columns = columns_names
    return verb_a_df,verb_b_df

def conjug_dfs_f(word):
    verb_a_df,verb_b_df= conjug_dfs(word)
    h_a,h_b= conjug_dfs('haber')
    verb_b_df.loc['Indicativo pretérito perfecto compuesto']=h_b.loc['Indicativo presente']+' '+verb_b_df.loc['Indicativo pretérito perfecto compuesto']
    verb_b_df.loc['Indicativo pretérito pluscuamperfecto']=h_b.loc['Indicativo pretérito imperfecto']+' '+verb_b_df.loc['Indicativo pretérito pluscuamperfecto']
    verb_b_df.loc['Indicativo futuro perfecto']=h_b.loc['Indicativo futuro']+' '+verb_b_df.loc['Indicativo futuro perfecto']
    verb_b_df.loc['Subjuntivo pretérito perfecto']=h_b.loc['Subjuntivo presente']+' '+verb_b_df.loc['Subjuntivo pretérito perfecto']
    verb_b_df.loc['Subjuntivo pretérito pluscuamperfecto 1']=h_b.loc['Subjuntivo pretérito imperfecto 1']+' '+verb_b_df.loc['Subjuntivo pretérito pluscuamperfecto 1']
    verb_b_df.loc['Condicional perfecto']=h_b.loc['Condicional Condicional']+' '+verb_b_df.loc['Condicional perfecto']
    verb_b_df.loc['Imperativo non']='no'+' '+verb_b_df.loc['Imperativo non']
    verb_b_df.loc['Imperativo non','yo']='-'
    return verb_a_df,verb_b_df


# check conjugation

mode_tense = ['Indicativo presente','Indicativo pretérito perfecto simple','Indicativo pretérito imperfecto','Indicativo futuro',
              'Condicional Condicional','Subjuntivo presente','Subjuntivo pretérito imperfecto 1','Subjuntivo futuro',
              'Imperativo Afirmativo']
mode_tense_1 = ['Indicativo presente','Indicativo pretérito perfecto compuesto','Indicativo pretérito perfecto simple',
                'Indicativo pretérito imperfecto','Indicativo pretérito pluscuamperfecto',
                'Indicativo futuro','Indicativo futuro perfecto','Condicional Condicional','Condicional perfecto',
                'Subjuntivo presente','Subjuntivo pretérito perfecto','Subjuntivo pretérito imperfecto 1',
                'Subjuntivo pretérito pluscuamperfecto 1',
                'Subjuntivo futuro','Imperativo Afirmativo','Imperativo non']


    
