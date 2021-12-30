import streamlit as st
import py3Dmol
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem

st.title("SMILES  + RDKit + Py3DMOL :smiley:")

# 用户输入SMILE （SMILE的细节不重要-就是一个电脑可读的分子结构描述）https://zh.wikipedia.org/wiki/%E7%AE%80%E5%8C%96%E5%88%86%E5%AD%90%E7%BA%BF%E6%80%A7%E8%BE%93%E5%85%A5%E8%A7%84%E8%8C%83
smile = st.text_input("SMILES please", "CC")

# 最后一行是展示2D化学结构 （其他细节不重要）
def draw_2d_mol(smile):
    mol = Chem.MolFromSmiles(smile)
    Draw.MolToFile(mol, "temp/mol.png")
    st.image("temp/mol.png")


# 最后一行是展示3D化学结构 （其他细节不重要）
def draw_3d_mol(smile, style="stick"):
    mol = Chem.MolFromSmiles(smile)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    AllChem.MMFFOptimizeMolecule(mol, maxIters=200)
    mblock = Chem.MolToMolBlock(mol)

    view = py3Dmol.view(width=400, height=400)
    view.addModel(mblock, "mol")
    view.setStyle({style: {}})
    view.zoomTo()
    view.show()
    view.render()
    t = view.js()
    f = open("temp/viz.html", "w")
    f.write(t.startjs)
    f.write(t.endjs)
    f.close()

    HtmlFile = open("temp/viz.html", "r", encoding="utf-8")
    source_code = HtmlFile.read()

    st.components.v1.html(source_code, height=400, width=400)


# Column 可以让这两个Component左右并排
# 看一下 https://docs.streamlit.io/library/api-reference/layout/st.columns
col1, col2 = st.columns(2)
with col1:
    st.write("Molecule :coffee:")
    draw_2d_mol(smile)
with col2:
    draw_3d_mol(smile)

st.text(
    "Author: José Manuel Nápoles ([@napoles3d](https://twitter.com/napoles3D))"
)
