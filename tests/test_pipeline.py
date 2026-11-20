import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from argparse import Namespace

spec = importlib.util.spec_from_file_location("pipeline", Path(__file__).parents[1] / "skills/massinha-30/scripts/pipeline.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
EXAMPLE = Path(__file__).parents[1] / "exemplos/retalhos.json"

class StateTest(unittest.TestCase):
    def test_approval_invalidated_by_story_change(self):
        with tempfile.TemporaryDirectory() as t:
            m.iniciar(Namespace(roteiro=EXAMPLE, out=t))
            with self.assertRaises(ValueError): m.load_run(t)
            m.aprovar(Namespace(pasta=t, evidencia="Aprovo o roteiro (fixture de teste)"))
            m.load_run(t)
            p=Path(t)/"roteiro.json"; s=json.loads(p.read_text()); s["cenas"][0]["texto"]="Texto alterado"; m.save(p,s)
            with self.assertRaises(ValueError): m.load_run(t)

    def test_existing_run_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as t:
            m.iniciar(Namespace(roteiro=EXAMPLE, out=t))
            with self.assertRaises(ValueError): m.iniciar(Namespace(roteiro=EXAMPLE, out=t))

    def test_uncertain_video_submission_does_not_charge_again(self):
        with tempfile.TemporaryDirectory() as t:
            m.iniciar(Namespace(roteiro=EXAMPLE, out=t)); m.aprovar(Namespace(pasta=t,evidencia="Aprovo (fixture)"))
            image=Path(t)/"01.png"; image.touch(); m.save(Path(t)/"kling-01.json",{"estado":"submissao-iniciada"})
            with self.assertRaises(ValueError): m.kling(Namespace(pasta=t,cena=1,imagem=image,enviar=True))

    def test_voice_retry_budget_stops_before_network(self):
        with tempfile.TemporaryDirectory() as t:
            m.iniciar(Namespace(roteiro=EXAMPLE, out=t)); m.aprovar(Namespace(pasta=t,evidencia="Aprovo (fixture)"))
            with self.assertRaises(ValueError): m.voz(Namespace(pasta=t,tomada=4,velocidade=1.0,enviar=True))

    def test_empty_alignment_is_rejected(self):
        with self.assertRaises(ValueError): m.captions({"characters":[],"character_start_times_seconds":[],"character_end_times_seconds":[]})

    def test_env_quoted_spaces_and_inline_comments(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"config.env"; p.write_text('EXAMPLE_VOICE_ID="abc123 " # narrator\nEXAMPLE_KEY="abc#123"\n')
            values=m.env_values(p)
            self.assertEqual(values["EXAMPLE_VOICE_ID"],"abc123")
            self.assertEqual(values["EXAMPLE_KEY"],"abc#123")

    def test_story_cuts_follow_measured_voice(self):
        story={"cenas":[{"texto":"A."},{"texto":"B."},{"texto":"C."},{"texto":"D."},{"texto":"E."},{"texto":"F."}]}
        text="A. B. C. D. E. F."
        a={"characters":list(text),"character_start_times_seconds":[i*.4 for i in range(len(text))]}
        durations=m.scene_durations(story,a)
        self.assertAlmostEqual(sum(durations),30)
        self.assertAlmostEqual(durations[0],1.2)
        a["characters"][0]="X"
        with self.assertRaises(ValueError):m.scene_durations(story,a)

    def test_real_character_timestamps_are_preserved(self):
        chars=list("Olá mundo.")
        a={"characters":chars,"character_start_times_seconds":[2+i*.1 for i in range(len(chars))],"character_end_times_seconds":[2.1+i*.1 for i in range(len(chars))]}
        s=m.captions(a)
        self.assertIn("00:00:02,000 --> 00:00:03,000",s)
        self.assertIn("Olá mundo.",s)

if __name__=="__main__": unittest.main()
